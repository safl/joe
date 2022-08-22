"""
    fio-wrapper for CIJOE
"""


def cfg(cijoe):
    """Check that the environment has the required entities"""

    return cijoe.config.options("fio")


def run(cijoe, args=None, cwd=None, evars=None):
    """Run 'fio' via CIJOE"""

    fio_cfg = cfg(cijoe)

    if args is None:
        args = []

    return cijoe.run(" ".join([fio_cfg["bin"]] + args), cwd, evars)
