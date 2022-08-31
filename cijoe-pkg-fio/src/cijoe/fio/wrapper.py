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

    log.error(f"does fio have it? env({env})")

    return cijoe.run(f"{cijoe.config.options['fio']['bin']} {args}", env=env)
