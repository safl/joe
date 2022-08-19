#!/usr/bin/env python3
"""
    Kill a qemu guest

    Retargetable: false
    -------------------
"""
from joe.qemu.wrapper import Guest


def worklet_entry(args, cijoe, step):
    """Kill a qemu guest"""

    guest = Guest(cijoe, cijoe.config)

    return guest.kill()
