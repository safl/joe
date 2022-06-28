"""
 fio-wrapper for CIJOE
"""


def env(cijoe):
    """Check that the environment has the required entities"""

    return cijoe.get_env("fio")


def run(cijoe, args=None, cwd=None, evars=None):
    """Run 'fio' via CIJOE"""

    fio = env(cijoe)

    if args is None:
        args = []

    return cijoe.run(" ".join([fio["bin"]] + args), cwd, evars)
