#!/usr/bin/env python3
"""
    Builds qemu system(x86_64-softmmu), disabling most graphics related features, and
    enabling virtfs and debugging.
"""
from pathlib import Path


def worklet_entry(cijoe, args, step):
    """Build qemu"""

    conf = cijoe.config.get("qemu", None)
    if not conf:
        return False

    build_dir = Path(conf["repository"]) / "build"

    configure_args = [
        '--audio-drv-list=""',
        "--disable-docs",
        "--disable-opengl",
        "--disable-virglrenderer",
        "--disable-vte",
        "--disable-gtk",
        "--disable-sdl",
        "--disable-spice",
        "--disable-vnc",
        "--disable-curses",
        "--disable-xen",
        "--disable-smartcard",
        "--disable-libnfs",
        "--disable-libusb",
        "--disable-glusterfs",
        "--enable-virtfs",
        "--enable-debug",
        "--prefix={conf['build']['prefix']}",
        "--target-list=x86_64-softmmu",
    ]

    cijoe.run(f"mkdir -p {build_dir}")
    cijoe.run("./configure " + " ".join(configure_args), cwd=build_dir)
    cijoe.run("make -j $(nproc)", cwd=build_dir)

    return True
