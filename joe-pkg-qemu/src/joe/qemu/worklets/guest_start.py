#!/usr/bin/env python3
"""
    Start a qemu-guest
"""
from joe.qemu.wrapper import Guest


def worklet_entry(args, cijoe, step):
    """Start a qemu guest"""

    guest = Guest(cijoe, cijoe.config)

    return guest.start()
