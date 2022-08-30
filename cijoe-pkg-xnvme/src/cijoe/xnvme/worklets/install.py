#!/usr/bin/env python3
"""
    Build xNVMe
"""
import errno
from pathlib import Path


def worklet_entry(args, cijoe, step):
    """Install qemu"""

    conf = cijoe.config.options.get("xnvme", None)
    if not conf:
        return errno.EINVAL

    repos_path = Path(conf["repository"]["path"])

    commands = [
        "make install",
    ]
    for cmd in commands:
        rcode, _ = cijoe.run(cmd, cwd=repos_path)
        if rcode:
            return rcode

    return rcode
