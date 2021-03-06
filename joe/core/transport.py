import os
import shutil
import subprocess
from abc import ABC, abstractmethod

import paramiko
from scp import SCPClient

from joe.core.misc import ENCODING


class Transport(ABC):
    @abstractmethod
    def cmd(self, cmd, cwd, evars, logfile):
        pass

    @abstractmethod
    def push(self, src, dst=None):
        pass

    @abstractmethod
    def pull(self, src, dst=None):
        pass


class Local(Transport):
    """Provide cmd/push/pull locally"""

    def __init__(self, env, output_path):
        self.env = env
        self.output_path = output_path
        self.output_ident = "aux"

    def cmd(self, cmd, cwd, evars, logfile):
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

    def push(self, src, dst=None):
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

    def pull(self, src, dst=None):
        """..."""

        return self.push(src, dst)


class SSH(Transport):
    """Provide cmd/push/pull over SSH"""

    def __init__(self, env, output_path):
        """Initialize the CIJOE SSH Transport"""

        self.env = env
        self.output_path = output_path

        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.WarningPolicy())

        self.ssh.load_system_host_keys()
        self.ssh.connect(**env.get("transport").get("ssh"))

        self.scp = SCPClient(self.ssh.get_transport())

    def cmd(self, cmd, cwd, evars, logfile):
        """Invoke the given command"""

        if cwd:
            cmd = f"cd {cwd}; {cmd}"

        stdin, stdout, stderr = self.ssh.exec_command(cmd, environment=evars)

        logfile.write(stdout.read().decode(ENCODING))
        logfile.write(stderr.read().decode(ENCODING))

        return stdout.channel.recv_exit_status()

    def push(self, src, dst=None):
        """Hmm... no return-value just exceptions"""

        if dst is None:
            dst = os.path.basename(src)
        if not os.path.isabs(src):
            src = os.path.join(self.output_path, self.output_ident, src)

        self.scp.put(src, dst)

        return True

    def pull(self, src, dst=None):
        """Hmm... no return-value just exceptions"""

        if dst is None:
            dst = os.path.basename(src)
        if not os.path.isabs(src):
            dst = os.path.join(self.output_path, self.output_ident, dst)

        self.scp.get(src, dst)

        return True
