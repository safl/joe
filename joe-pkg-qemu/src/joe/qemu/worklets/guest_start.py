#!/usr/bin/env python3
"""
    Start a qemu-guest

    Retargetable: false
    -------------------
"""
import errno

from joe.qemu.wrapper import Guest


def worklet_entry(args, cijoe, step):
    """Start a qemu guest"""

    guest = Guest(cijoe, cijoe.config)

    rcode = guest.start()
    if rcode:
        log.error(f"guest.start() : rcode({rcode})")
        return rcode

    started = guest.is_up()
    if not started:
        log.error("guest.is_up() : False")
        return errno.EAGAIN

    return 0
