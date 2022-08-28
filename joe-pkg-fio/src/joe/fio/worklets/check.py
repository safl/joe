#!/usr/bin/env python3
"""
    Check the version of the wrapped fio
"""
from joe.fio.wrapper import fio


def worklet_entry(args, cijoe, step):
    """Check version of fio"""

    rcode, _ = fio(cijoe, "--help")

    return rcode
