#!/usr/bin/env python3
"""
    Installs qemu
"""
import errno
from pathlib import Path


def worklet_entry(args, cijoe, step):
    """Install qemu"""

    conf = cijoe.config.options.get("qemu", None)
    if not conf:
        return errno.EINVAL

    build_dir = Path(conf["repository"]["path"]) / "build"

    rcode, _ = cijoe.run_local("make install", cwd=build_dir)

    return rcode