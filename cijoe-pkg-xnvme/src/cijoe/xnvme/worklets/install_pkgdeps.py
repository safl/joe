#!/usr/bin/env python3
"""
install xNVMe package dependencies
==================================

Currently only functional on Debian bullseye. Expect failure on anything else.

Retargetable: True
------------------
"""
import errno
from pathlib import Path


def worklet_entry(args, cijoe, step):
    """Install qemu"""

    repos = cijoe.config.options.get("xnvme", {}).get("repository", None)
    if not repos:
        return errno.EINVAL

    rcode, _ = cijoe.run("./toolbox/pkgs/debian-bullseye.sh", cwd=repos["path"])
    if rcode:
        return rcode

    return 0
