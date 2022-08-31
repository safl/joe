import logging
import os
import shutil
import subprocess
from abc import ABC, abstractmethod
from pathlib import Path

import paramiko
from scp import SCPClient

from cijoe.core.misc import ENCODING
from cijoe.core.resources import Config


class Transport(ABC):
    @abstractmethod
    def run(self, cmd, cwd, evars, logfile):
        pass

    @abstractmethod
    def get(self, src, dst=None):
        pass

    @abstractmethod
    def put(self, src, dst=None):
        pass


class Local(Transport):
    """Provide cmd/push/pull locally"""

    def __init__(self, config: Config, output_path: Path):
        self.config = config
        self.output_path = output_path
        self.output_ident = "artifacts"

    def run(self, cmd, cwd, evars, logfile):
        """Invoke the given command"""

        with subprocess.Popen(
            cmd,
            stdout=logfile,
            stderr=subprocess.STDOUT,
            shell=True,
            cwd=cwd,
        ) as process:
            process.wait()

            return process.returncode

    def put(self, src, dst=None):
        """..."""

        if dst is None:
            dst = os.path.basename(src)
        if not os.path.isabs(src):
            src = os.path.join(self.output_path, self.output_ident, src)
        if not os.path.isabs(dst):
            dst = os.path.join(self.output_path, self.output_ident, dst)

        if src == dst:
            return True

        if os.path.isdir(src):
            shutil.copytree(src, dst)
            return True

        shutil.copy(src, dst)
        return True

    def get(self, src, dst=None):
        """..."""

        return self.put(src, dst)


class SSH(Transport):
    """Provide cmd/push/pull over SSH"""

    def __init__(self, config, output_path):
        """Initialize the CIJOE SSH Transport"""

        self.config = config
        self.output_path = output_path

        self.ssh = paramiko.SSHClient()

        # Using the 'AutoAddPolicy()' *without* load_system_host_keys(), by doing so,
        # then Paramiko does not know any hosts, and simply adds them first time they
        # are connected to.
        # It was attempted to use load_system_host_keys() with WarningPolicy(), however,
        # when a host changed, e.g. re-provisioned virtual machine, then the host-key
        # changes and Paramiko cannot connect.
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.scp = None

        # Not connecting at this point, since the remote side might be ready at the time
        # the transport is initialized. For example, when a qemu-guest is booted, then
        # cijoe.run_local() is used, and not until the guest is up will the cij.run() be
        # used. Also, when a system reboots etc. then dropped connections must be
        # handled, lastly connection close must happen as Python terminates, dangling
        # connections will make it hang.
        # Thus, __connect()/__disconnect() is called for each call to run()/get()/put().
        # Current short-coming is of course that then these cannot happen in parallel.

        paramiko.util.log_to_file(
            self.output_path / "paramiko.log", level=logging.root.level
        )

    def __connect(self):

        self.ssh.connect(**self.config.options.get("transport").get("ssh"))
        self.scp = SCPClient(self.ssh.get_transport())

    def __disconnect(self):

        self.scp.close()
        self.ssh.close()

    def run(self, cmd, cwd, evars, logfile):
        """Invoke the given command"""

        if cwd:
            cmd = f"cd {cwd}; {cmd}"

        self.__connect()

        _, stdout, stderr = self.ssh.exec_command(cmd, environment=evars)

        logfile.write(stdout.read().decode(ENCODING))
        logfile.write(stderr.read().decode(ENCODING))

        rcode = stdout.channel.recv_exit_status()

        self.__disconnect()

        return rcode

    def put(self, src, dst=None):
        """Hmm... no return-value just exceptions"""

        self.__connect()

        if dst is None:
            dst = os.path.basename(src)
        if not os.path.isabs(src):
            src = os.path.join(self.output_path, self.output_ident, src)

        self.scp.put(src, dst)

        self.__disconnect()

        return True

    def get(self, src, dst=None):
        """Hmm... no return-value just exceptions"""

        self.__connect()

        if dst is None:
            dst = os.path.basename(src)
        if not os.path.isabs(src):
            dst = os.path.join(self.output_path, self.output_ident, dst)

        self.scp.get(src, dst)

        self.__disconnect()

        return True
