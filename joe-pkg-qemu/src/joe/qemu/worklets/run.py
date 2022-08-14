#!/usr/bin/env python3
"""
    Run a qemu guest
"""
import errno
from pathlib import Path


def worklet_entry(args, collector, cijoe, step):
    """Build qemu"""

    conf = cijoe.config.get("qemu", None)
    if not conf:
        return errno.EINVAL

    boot_iso = Path(conf["path"]) / "emujoe" / "boot.iso"
    boot_img = Path(conf["path"]) / "emujoe" / "boot.img"
    pid = Path(conf["path"]) / "emujoe" / "guest.pid"
    monitor = Path(conf["path"]) / "emujoe" / "monitor.sock"
    serial = Path(conf["path"]) / "emujoe" / "serial.sock"

    args = []

    args += [
        "-machine", "type=q35,kernel_irqchip=split,accel=kvm"
        "-cpu", "host",
        "-smp", "4",
        "-device", "intel-iommu,pt=on,intremap=on",
        "-m", "6GB",
    )

    # magic-option, enable intel-iommu
    args += ["-device", "intel-iommu,pt=on,intremap=on"]

    # magic-option, when 'boot.iso' exists, then add the -boot arg
    if boot_iso.exists():
        args += [
            "-boot", "d", "-cdrom", str(boot_iso)
        ]

    # magic-option, when 'boot.img' exists, add it is as boot-drive
    if boot_img.exists():
        args += [
            "-blockdev",
            f"qcow2,node-name=boot,file.driver=file,file.filename={boot_img}"
        ]
        args += ["-device", "virtio-blk-pci,drive=boot"]

    # TCP host-forward
    args += ["-netdev", "user,id=n1,ipv6=off,hostfwd=tcp::2022-:22"]
    args += ["-device", "virtio-net-pci,netdev=n1"

    ## Management stuff
    args += ["-pidfile", str(pid)]

    args += ["-monitor", f"unix:{monitor},server,nowait"]

    if True:
        args += ["-display", "none"]
        args += ["-serial", f"file:{serial},server,nowait"]
        args += ["-daemonize"]
    else:
        args += ["-nographic"]
        args += ["-serial", "mon:stdio"]

    rcode, _ = cijoe.run_local(" ".join(args))

    return rcode
