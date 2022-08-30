#!/usr/bin/env python3
"""
install fio
===========

Just a plain 'make install' within 'repository.path'

Retargetable: True
------------------
"""
from pathlib import Path


def worklet_entry(args, cijoe, step):
    """Install fio"""

    rcode, _ = cijoe.run(
        "make install", cwd=Path(cijoe.config.options["fio"]["repository"]["path"])
    )
    return rcode
