import os
import shutil
import subprocess
from abc import ABC, abstractmethod
from pathlib import Path

import paramiko
from scp import SCPClient

from joe.core.misc import ENCODING
from joe.core.resources import Config


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
        self.output_ident = "aux"

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
        # self.ssh.set_missing_host_key_policy(paramiko.WarningPolicy)
        # self.ssh.load_system_host_keys()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        self.scp = None

        paramiko.util.log_to_file("/tmp/paramiko.log", level="WARN")

    def __connect(self):

        self.ssh.connect(**self.config.options.get("transport").get("ssh"))
        self.scp = SCPClient(self.ssh.get_transport())

    def run(self, cmd, cwd, evars, logfile):
        """Invoke the given command"""

        if cwd:
            cmd = f"cd {cwd}; {cmd}"

        if not self.scp:
            self.__connect()
        stdin, stdout, stderr = self.ssh.exec_command(cmd, environment=evars)

        logfile.write(stdout.read().decode(ENCODING))
        logfile.write(stderr.read().decode(ENCODING))

        return stdout.channel.recv_exit_status()

    def put(self, src, dst=None):
        """Hmm... no return-value just exceptions"""

        if dst is None:
            dst = os.path.basename(src)
        if not os.path.isabs(src):
            src = os.path.join(self.output_path, self.output_ident, src)

        self.scp.put(src, dst)

        return True

    def get(self, src, dst=None):
        """Hmm... no return-value just exceptions"""

        if dst is None:
            dst = os.path.basename(src)
        if not os.path.isabs(src):
            dst = os.path.join(self.output_path, self.output_ident, dst)

        self.scp.get(src, dst)

        return True
