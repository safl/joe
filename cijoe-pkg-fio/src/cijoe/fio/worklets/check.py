#!/usr/bin/env python3
"""
    fio: check
    ==========

    Check the version of the wrapped fio

    Retargetable: True
    ------------------
"""
from cijoe.fio.wrapper import fio


def worklet_entry(args, cijoe, step):
    """Check version of fio"""

    rcode, _ = fio(cijoe, "--help")

    return rcode
