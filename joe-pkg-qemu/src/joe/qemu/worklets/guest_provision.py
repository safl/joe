#!/usr/bin/env python3
"""
    Provision a qemu-guest
"""
import errno
from pathlib import Path

from joe.qemu.wrapper import Guest


def worklet_entry(args, cijoe, step):
    """Provision a qemu-guest using a cloud-init image"""

    guest = Guest(cijoe, cijoe.config)

    return guest.provision()
