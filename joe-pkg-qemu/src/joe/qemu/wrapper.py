"""
    A wrapper around qemu_system, qemu_img with helpers for controlling a guest

    Note that this is a 'local-only' wrapper, it **cannot** be retargeted onto a remote
    machine.
"""
import os
from pathlib import Path

import psutil

from joe.core.misc import h3

GUEST_NAME_DEFAULT = "emujoe"


def qemu_img(cijoe, args=[]):
    """Helper function wrapping around 'qemu_img'"""

    return cijoe.run_local(
        f"{cijoe.config.options['qemu']['img_bin']} " + " ".join(args)
    )


def qemu_system(cijoe, args=[]):
    """Wrapping the qemu system binary"""

    return cijoe.run_local(
        f"{cijoe.config.options['qemu']['system_bin']}" + " ".join(args)
    )


class Guest(object):
    def __init__(self, cijoe, config):
        """."""

        self.cijoe = cijoe

        self.qemu_cfg = config.options.get("qemu", None)
        self.guest_cfg = self.qemu_cfg["guests"]["emujoe"]

        self.guest_path = (Path(self.guest_cfg["path"])).resolve()
        self.boot_iso = self.guest_path / "boot.iso"
        self.boot_img = self.guest_path / "boot.img"
        self.pid = self.guest_path / "guest.pid"
        self.monitor = self.guest_path / "monitor.sock"
        self.serial = self.guest_path / "serial.sock"

    def is_initialized(self):
        """Check that the guest is initialized"""

        return self.guest_path.exists()

    def is_running(self):
        """Check whether the guest is running"""

        return self.get_pid() and psutil.pid_exists(pid)

    def get_pid(self):
        """Returns pid from 'guest.pid', returns 0 when 'guest.pid' is not found"""

        if not self.pid.exists():
            return 0

        with self.pid.open() as pidfile:
            pid = pidfile.read().strip()

        return pid

    def initialize(self):
        """Create a 'home' for the guest'"""

        os.makedirs(self.guest_path, exist_ok=True)

    def start(self):
        """."""

        args = [self.qemu_cfg["system_bin"]]

        args += [
            "-machine",
            "type=q35,kernel_irqchip=split,accel=kvm",
            "-cpu",
            "host",
            "-smp",
            "4",
            "-m",
            "6G",
        ]

        # magic-option, enable intel-iommu
        args += ["-device", "intel-iommu,pt=on,intremap=on"]

        # magic-option, when 'boot.iso' exists, then add the -boot arg
        if self.boot_iso.exists():
            args += ["-boot", "d", "-cdrom", str(self.boot_iso)]

        # magic-option, when 'boot.img' exists, add it is as boot-drive
        if self.boot_img.exists():
            args += [
                "-blockdev",
                f"qcow2,node-name=boot,file.driver=file,file.filename={self.boot_img}",
            ]
            args += ["-device", "virtio-blk-pci,drive=boot"]

        # TCP host-forward
        args += ["-netdev", "user,id=n1,ipv6=off,hostfwd=tcp::2022-:22"]
        args += ["-device", "virtio-net-pci,netdev=n1"]

        # Management stuff
        args += ["-pidfile", str(self.pid)]

        args += ["-monitor", f"unix:{self.monitor},server,nowait"]

        if True:
            args += ["-display", "none"]
            args += ["-serial", f"file:{self.serial},server,nowait"]
            args += ["-daemonize"]
        else:
            args += ["-nographic"]
            args += ["-serial", "mon:stdio"]

        rcode, _ = self.cijoe.run_local(" ".join(args))

        return rcode

    def kill(self):
        """Shutdown qemu guests by killing the process using the 'guest.pid'"""

        rcode = 0

        pid = sel.get_pid()
        if pid:
            rcode, _ = self.cijoe.run_local(f"kill {pid}")

        return rcode

    def provision(self):
        """Provision a guest"""

        self.initialize()

        # TODO: download cloud-img
        # TODO: construct meta-data by copying it from resources
        # TODO: construct user-data by copying it from resources and adding
        # ~/.ssh/id_rsa.pub
        # Then

        # copy stuff and boot the machine
