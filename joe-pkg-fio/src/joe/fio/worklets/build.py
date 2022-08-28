#!/usr/bin/env python3
"""
    Installs qemu
"""
from pathlib import Path


def worklet_entry(args, cijoe, step):
    """Install qemu"""

    commands = [
        "make clean",
        f"./configure --prefix={ cijoe.config.options['fio']['build']['prefix'] }",
        "make -j $(nproc)",
    ]
    for cmd in commands:
        rcode, _ = cijoe.run_local(
            cmd, cwd=Path(cijoe.config.options["fio"]["repository"]["path"])
        )
        if rcode:
            return rcode

    return rcode
