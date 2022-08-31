"""
    fio-wrapper
    ===========

    config
    ------

    fio.bin

    fio.engines

    retargtable: true
    -----------------
"""
import errno
import logging as log


def fio(cijoe, args="", env={}):
    """Invoke 'fio'"""

    return cijoe.run(f"{cijoe.config.options['fio']['bin']} {args}", env=env)
