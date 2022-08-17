from pathlib import Path

from joe.core.misc import h3

GUEST_NAME_DEFAULT = "emujoe"


def qemu_img(cijoe, args=[]):
    """Helper function wrapping around 'qemu_img'"""

    return cijoe.run_local(f"{cijoe.config.options['qemu']['img_bin']} " + " ".join(args))


def qemu_system(cijoe, args=[]):
    """Wrapping the qemu system binary"""

    return cijoe.run_local(f"{cijoe.config.options['qemu']['system_bin']}" + " ".join(args))


def guest_init(cijoe, guest_name=None):
    """Create guest file layout"""

    if guest_name is None:
        guest_name = GUEST_NAME_DEFAULT

    guest = cijoe.config.options["qemu"].get(guest_name)
    guest["path"] = Path(guest["path"])

    rcode, _ = cijoe.run_local(f"mkdir -p {guest['path']}")

    return rcode


class Guest(object):
    def __init__(self, cijoe, config):
        """."""

        self.cijoe = cijoe

        self.qemu_cfg = config.options.get("qemu", None)
        self.guest_cfg = self.qemu_cfg["guests"]["emujoe"]

        self.boot_iso = Path(self.guest_cfg["path"]) / "boot.iso"
        self.boot_img = Path(self.guest_cfg["path"]) / "boot.img"
        self.pid = Path(self.guest_cfg["path"]) / "guest.pid"
        self.monitor = Path(self.guest_cfg["path"]) / "monitor.sock"
        self.serial = Path(self.guest_cfg["path"]) / "serial.sock"

    def is_running(self):
        """..."""

        with self.pid.open() as pidfile:
            pid = pidfile.read()

        h3(f"pid: {pid}")

        return True

    def kill(self):
        """Shutdown qemu guests by killing the process using the 'guest.pidfile'"""

        with self.pid.open() as pidfile:
            pid = pidfile.read().strip()

        rcode, _ = self.cijoe.run_local(f"kill {pid}")

        return rcode

    def run(self):
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
