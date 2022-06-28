"""
 fio-wrapper for CIJOE
"""


def env(cijoe):
    """Check that the environment has the required entities"""

    return cijoe.get_env("fio")


def run(cijoe, args, cwd, evars):
    """Run 'fio' via CIJOE"""

    fio = env(cijoe)

    return cijoe.cmd(" ".join([fio["bin"]] + args), evars)
