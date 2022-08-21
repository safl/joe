"""

"""
import errno
import os
import time
from pathlib import Path

from joe.core import transport
from joe.core.misc import ENCODING
from joe.core.resources import Config


def default_output_path():
    """Returns a default output-path"""

    return os.path.join(os.getcwd(), "cijoe-output")


class Cijoe(object):
    """CIJOE providing retargetable command-line expressions and data-transfers"""

    def __init__(self, config: Config, output_path: Path):
        """Create a cijoe encapsulation defined by the given config_fpath"""

        self.config = config

        self.run_count = 0
        self.output_path = output_path if output_path else default_output_path()
        self.output_ident = "artifacts"

        os.makedirs(os.path.join(self.output_path, self.output_ident), exist_ok=True)

        self.transport_local = transport.Local(self.config, self.output_path)
        self.transport = self.transport_local

        ssh = self.config.options.get("transport", {}).get("ssh", None)
        if ssh:
            self.transport = transport.SSH(self.config, self.output_path)

    def set_output_ident(self, output_ident: str):
        """
        This sets the output-identifier which is used in order to provide a subfolder
        for artifacts, command-output etc. Additionally, then it reset the command
        run-count
        """

        self.run_count = 0
        self.output_ident = output_ident
        self.transport.output_ident = output_ident

    def _run(self, cmd, cwd=None, evars=None, transport=None):

        self.run_count += 1
        cmd_output_dpath = os.path.join(self.output_path, self.output_ident)
        cmd_output_fpath = os.path.join(
            cmd_output_dpath, f"cmd_{self.run_count:02}.output"
        )
        cmd_state_fpath = os.path.join(
            cmd_output_dpath, f"cmd_{self.run_count:02}.state"
        )
        os.makedirs(cmd_output_dpath, exist_ok=True)

        with open(cmd_output_fpath, "a", encoding=ENCODING) as logfile:
            begin = time.time()

            try:
                rcode = transport.run(cmd, cwd, evars, logfile)
            except Exception as exc:
                if (
                    hasattr(exc, "errno")
                    and isinstance(exc.errno, int)
                    and exc.errno > 0
                ):
                    rcode = exc.errno
                else:
                    rcode = errno.EIO
                logfile.write(f"# transport.run(); raised({exc})\n")

            end = time.time()

            state = {
                "cmd": cmd,
                "cwd": cwd,
                "rcode": rcode,
                "begin": begin,
                "end": end,
                "elapsed": end - begin,
                "output_fpath": cmd_output_fpath,
            }
            with open(cmd_state_fpath, "a", encoding=ENCODING) as state_file:
                state_file.write(str(state))

        return rcode, state

    def run(self, cmd, cwd=None, evars=None):
        """
        Execute the given shell command/expression via 'config.transport'

        Commands executed using this will write stdout and stderr to file. The location
        of the logfile is fixed to: "output_path/output_ident/cmd.log", such that the
        location is a subfolder of the output_path. Unless somebody wants to break the
        convention and call set_output_ident("../..")
        """

        return self._run(cmd, cwd, evars, self.transport)

    def run_local(self, cmd, cwd=None, evars=None):
        """
        Execute the given shell command/expression via local transport

        Commands executed using this will write stdout and stderr to file. The location
        of the logfile is fixed to: "output_path/output_ident/cmd.log", such that the
        location is a subfolder of the output_path. Unless somebody wants to break the
        convention and call set_output_ident("../..")
        """

        return self._run(cmd, cwd, evars, self.transport_local)

    def put(self, src, dst):
        """Transfer 'src' on 'dev_box' to 'dst' on **test_target**"""

        os.makedirs(os.path.join(self.output_path, self.output_ident), exist_ok=True)

        return self.transport.put(src, dst)

    def get(self, src, dst):
        """Transfer 'src' on 'test_target' to 'dst' on **dev_box**"""

        os.makedirs(os.path.join(self.output_path, self.output_ident), exist_ok=True)

        return self.transport.get(src, dst)
