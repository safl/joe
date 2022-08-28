"""
    fio-wrapper
    ===========

    config
    ------

    fio.bin

    retargtable: true
    -----------------
"""


def fio(cijoe, args=""):
    """Invoke 'fio'"""

    return cijoe.run(f"{cijoe.config.options['fio']['bin']} {args}")
