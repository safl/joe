#!/usr/bin/env python3
"""
    Builds qemu system(x86_64-softmmu), disabling most graphics related features, and
    enabling virtfs and debugging.
"""
import errno
from pathlib import Path


def worklet_entry(args, collector, cijoe, step):
    """Build qemu"""

    conf = cijoe.config.get("qemu", None)
    if not conf:
        return errno.EINVAL

    build_dir = Path(conf["repository"]["path"]) / "build"

    rcode, _ = cijoe.run_local("make install", cwd=build_dir)

    return rcode
