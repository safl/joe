#!/usr/bin/env python3
"""
    Run a qemu guest
"""
import errno
from pathlib import Path

from joe.qemu.wrapper import Guest


def worklet_entry(args, cijoe, step):
    """Build qemu"""

    guest = Guest(cijoe, cijoe.config)

    return guest.run()
