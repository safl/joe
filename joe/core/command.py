"""
Prototype of a CIJOE refactor focusing on:

* Remove Bash from CIJOE
  - Requires re-implementing at least: core, qemu, fio

* Replace the test-runner 'cij_runner' with 'pytest'
  - This will most likely not be done in a compatible fashion with the trun-data-struct
  - Requires re-doing auxilary output generation and handling
  - Requires re-implementing extractors, analyzers, plotters etc.

Observations
------------

test_target environment variables; forwarding of environment variables, either defined
in the env.yaml or passed directly in a testcase can be passed with less friction than
in the Bash-based approach. Atleast for the Popen part, lets see how paramiko handles
it.

By using paramiko, a SSH session can be kept alive instead of re-establishing connection
for the command. This is a change in behavior which may or may not be great. I wonder
whether mosh could be used as a transport here as well.

It would seem like, with paramiko we can better separate whether the executed command
failed or the SSH layer. This is a very nice improvement.

The current Transport using command-execution via paramiko is something I am certain
will dead-lock, it needs a lot of love. Should read the buffers and write them to
logfile until the command ends. The returncode is missing as well.

This needs the data-movement parts implemented, then the command-stuff is done.
"""
import os
import time

import yaml

from joe.core import transport
from joe.core.misc import ENCODING


def env_from_file(env_fpath):
    """Load the environment definition from the given 'env_fpath'"""

    with open(env_fpath, "r") as env_file:
        return yaml.safe_load(env_file)


def default_output_path():
    """Returns a default output-path"""

    return os.path.join(
        os.getcwd(),
        "cijoe-output-" + time.strftime("%Y%m%d-%H%M%S", time.gmtime(time.time())),
    )


class Cijoe(object):
    """CIJOE providing retargetable command-line expressions and data-transfers"""

    def __init__(self, env, output_path):
        """Create a cijoe encapsulation defined by the given env"""

        env = env if env else {}
        self.env = env
        self.output_path = output_path
        self.output_ident = "aux"

        os.makedirs(os.path.join(self.output_path, self.output_ident), exist_ok=True)

        ssh = env.get("transport", {}).get("ssh", None)
        if ssh:
            self.transport = transport.SSH(env, self.output_path)
        else:
            self.transport = transport.Local(env, self.output_path)

    def get_env(self, subject=None):
        """Return the environment definition"""

        return self.env.get(subject, None)

    def set_output_ident(self, output_ident):
        """This is a path relative to the self.output"""

        self.output_ident = output_ident
        self.transport.output_ident = output_ident

    def cmd(self, cmd, cwd=None, evars=None):
        """
        Execute the given shell command/expression via 'env.transport'

        Commands executed using this will write stdout and stderr to file. The location
        of the logfile is fixed to: "output_path/output_ident/cmd.log", such that the
        location is a subfolder of the output_path. Unless somebody wants to break the
        convention and call set_output_ident("../..")
        """

        cmd_output_dpath = os.path.join(self.output_path, self.output_ident)
        cmd_output_fpath = os.path.join(cmd_output_dpath, "cmd.log")
        cmd_state_fpath = os.path.join(cmd_output_dpath, "cmd.state")
        os.makedirs(cmd_output_dpath, exist_ok=True)

        with open(cmd_output_fpath, "a", encoding=ENCODING) as logfile:
            logfile.write(f'# do: "{cmd}"\n')
            logfile.flush()

            begin = time.time()
            rcode = self.transport.cmd(cmd, cwd, evars, logfile)
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

    def push(self, src, dst):
        """Transfer 'src' on 'dev_box' to 'dst' on **test_target**"""

        os.makedirs(os.path.join(self.output_path, self.output_ident), exist_ok=True)

        return self.transport.push(src, dst)

    def pull(self, src, dst):
        """Transfer 'src' on 'test_target' to 'dst' on **dev_box**"""

        os.makedirs(os.path.join(self.output_path, self.output_ident), exist_ok=True)

        return self.transport.pull(src, dst)
