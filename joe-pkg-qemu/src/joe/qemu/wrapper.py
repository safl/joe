"""
    Wraps qemu binaries: system, qemu_img + provides "guest-control"

    NOTE: this wrapper is "local-only". That is, changing transport does not retarget
    the functionality provided here. Most of the code is utilizing Python modules such
    as shutil, pathlib, psutil, download/requests. To make this re-targetable these
    things must be done via command-line utilities. It is certainly doable, however,
    currently not a priority as the intent is to utilize qemu to produce a virtual
    machine to serve as a 'target' for tests.
"""
import os
import shutil
from pathlib import Path

import psutil

from joe.core.misc import download, h3

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

        self.qemu_config = config.options.get("qemu", None)
        self.guest_config = self.qemu_config["guests"]["emujoe"]

        self.guest_path = (Path(self.guest_config["path"])).resolve()
        self.boot_img = self.guest_path / "boot.img"
        self.cloudinit_img = self.guest_path / "cloudinit.img"
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

        args = [self.qemu_config["system_bin"]]

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

        pid = self.get_pid()
        if pid:
            rcode, _ = self.cijoe.run_local(f"kill {pid}")

        return rcode

    def provision(self):
        """Provision a guest"""

        self.kill()  # Ensure the guest is *not* running
        self.initialize()  # Ensure the guest has a "home"

        if not self.cloudinit_img.exists():  # Retrieve the cloudinit-image
            cloudinit_local = Path(self.guest_config["cloudinit"]["img"]).resolve()
            if cloudinit_local.exists():
                shutil.copyfile(str(cloudinit_local), self.cloudinit_img)
            else:
                err, path = download(
                    self.guest_config["cloudinit"]["url"], self.cloudinit_img
                )
                if err:
                    print(
                        f"download({self.guest_config['cloudinit']['url']}), {self.cloudinit_img}: failed"
                    )
                    return err

        shutil.copyfile(self.guest_config["cloudinit"]["user"], self.guest_path /
        "user-data")
        shutil.copyfile(self.guest_config["cloudinit"]["meta"], self.guest_path /
        "meta-data")

        # TODO: add the ssh-key to the meta

        # Boot the "installation"

        return 0

        # ~/.ssh/id_rsa.pub
        # Then

        # boot the machine and wait for it to "settle"
