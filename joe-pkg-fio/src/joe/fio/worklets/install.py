#!/usr/bin/env python3
"""
    Installs fio

    retargetable: True
    ==================
"""
from pathlib import Path


def worklet_entry(args, cijoe, step):
    """Install fio"""

    rcode, _ = cijoe.run_local(
        "make install", cwd=Path(cijoe.config.options["fio"]["repository"]["path"])
    )
    return rcode
