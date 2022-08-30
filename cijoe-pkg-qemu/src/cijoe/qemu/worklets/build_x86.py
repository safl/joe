#!/usr/bin/env python3
"""
    Builds qemu system(x86_64-softmmu), disabling most graphics related features, and
    enabling virtfs and debugging.

    Retargetable: false
    -------------------

    Arguments
    ---------

    repository.path
    build.prefix
"""
import errno
import logging as log
from pathlib import Path


def worklet_entry(args, cijoe, step):
    """Build qemu"""

    conf = cijoe.config.options.get("qemu", None)
    if not conf:
        log.error("config is missing 'qemu' section")
        return errno.EINVAL

    build_dir = Path(conf["repository"]["path"]) / "build"

    configure_args = [
        f"--prefix={conf['build']['prefix']}",
        "--audio-drv-list=''",
        "--disable-curses",
        "--disable-docs",
        "--disable-glusterfs",
        "--disable-gtk",
        "--disable-libnfs",
        "--disable-libusb",
        "--disable-opengl",
        "--disable-sdl",
        "--disable-smartcard",
        "--disable-spice",
        "--disable-virglrenderer",
        "--disable-vnc",
        "--disable-vte",
        "--disable-xen",
        "--enable-debug",
        "--enable-virtfs",
        "--target-list=x86_64-softmmu",
    ]

    rcode, _ = cijoe.run_local(f"mkdir -p {build_dir}")
    if rcode:
        return rcode

    rcode, _ = cijoe.run_local(
        "../configure " + " ".join(configure_args), cwd=build_dir
    )
    if rcode:
        return rcode

    rcode, _ = cijoe.run_local("make -j $(nproc)", cwd=build_dir)
    if rcode:
        return rcode

    return 0
