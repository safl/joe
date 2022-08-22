#!/usr/bin/env python3
"""
    Installs qemu
"""
import errno
from pathlib import Path


def worklet_entry(args, cijoe, step):
    """Install qemu"""

    conf = cijoe.config.options.get("fio", None)
    if not conf:
        return errno.EINVAL

    build_dir = Path(conf["repository"]["path"])

    commands = [
        "make clean",
        "./configure",
        "make -j $(nproc)",
    ]
    for cmd in commands:
        rcode, _ = cijoe.run_local(cmd, cwd=build_dir)
        if rcode:
            return rcode

    return rcode
