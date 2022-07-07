"""

"""
import os
import time
import logging

import yaml

from joe.core import transport
from joe.core.misc import ENCODING


def config_from_file(config_fpath):
    """Load the environment configuration from the given 'config_fpath'"""

    with open(config_fpath, "r") as config_file:
        return yaml.safe_load(config_file)


def default_output_path():
    """Returns a default output-path"""

    return os.path.join(
        os.getcwd(),
        "cijoe-output-" + time.strftime("%Y%m%d-%H%M%S", time.gmtime(time.time())),
    )


class Cijoe(object):
    """CIJOE providing retargetable command-line expressions and data-transfers"""

    def __init__(self, config_fpath=None, output_path=None):
        """Create a cijoe encapsulation defined by the given config_fpath"""

        self.config_fpath = os.path.abspath(config_fpath) if config_fpath else None
        self.config = config_from_file(self.config_fpath) if self.config_fpath else {}
        if not self.config:
            self.config = {}
        self.output_path = output_path if output_path else default_output_path()
        self.output_ident = "artifacts"

        self.logger = logging.FileHandler(os.path.join(self.output_path, "cijoe.log"))
        self.logger.setLevel(logging.INFO)


        os.makedirs(os.path.join(self.output_path, self.output_ident), exist_ok=True)

        ssh = self.config.get("transport", {}).get("ssh", None)
        if ssh:
            self.transport = transport.SSH(self.config, self.output_path)
        else:
            self.transport = transport.Local(self.config, self.output_path)

    def get_config(self, subject=None):
        """Return the environment configuration"""

        return self.config.get(subject, None)

    def get_config_fpath(self):
        """Return the environment configuration filepath, None when default is used."""

        return self.config_fpath

    def set_output_ident(self, output_ident):
        """This is a path relative to the self.output"""

        self.output_ident = output_ident
        self.transport.output_ident = output_ident

    def run(self, cmd, cwd=None, evars=None):
        """
        Execute the given shell command/expression via 'config.transport'

        Commands executed using this will write stdout and stderr to file. The location
        of the logfile is fixed to: "output_path/output_ident/cmd.log", such that the
        location is a subfolder of the output_path. Unless somebody wants to break the
        convention and call set_output_ident("../..")
        """

        cmd_output_dpath = os.path.join(self.output_path, self.output_ident)
        cmd_output_fpath = os.path.join(cmd_output_dpath, "run.log")
        cmd_state_fpath = os.path.join(cmd_output_dpath, "cmd.state")
        os.makedirs(cmd_output_dpath, exist_ok=True)

        with open(cmd_output_fpath, "a", encoding=ENCODING) as logfile:
            logfile.write(f'# do: "{cmd}"\n')
            logfile.flush()

            begin = time.time()
            rcode = self.transport.run(cmd, cwd, evars, logfile)
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

            logfile.write(f"# state: {state}\n")
            logfile.flush()

            with open(cmd_state_fpath, "a", encoding=ENCODING) as state_file:
                state_file.write(str(state))

        return rcode, state

    def put(self, src, dst):
        """Transfer 'src' on 'dev_box' to 'dst' on **test_target**"""

        os.makedirs(os.path.join(self.output_path, self.output_ident), exist_ok=True)

        return self.transport.put(src, dst)

    def get(self, src, dst):
        """Transfer 'src' on 'test_target' to 'dst' on **dev_box**"""

        os.makedirs(os.path.join(self.output_path, self.output_ident), exist_ok=True)

        return self.transport.get(src, dst)
