#!/usr/bin/env python3
"""
    Builds qemu system(x86_64-softmmu), disabling most graphics related features, and
    enabling virtfs and debugging.
"""
import os


def worklet_entry(cijoe, args, step):
    """Build qemu"""

    conf = cijoe.config.get("qemu", None)
    if not conf:
        return False

    build_dir = os.path.join(conf["repository"], "build")

    cijoe.run("make install", cwd=build_dir)

    return True
