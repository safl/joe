from pathlib import Path

GUEST_NAME_DEFAULT = "emujoe"


def qemu_img(cijoe, args=[]):
    """Helper function wrapping around 'qemu_img'"""

    return cijoe.run_local(f"{cijoe.config['qemu']['img_bin']} " + " ".join(args))


def qemu_system(cijoe, args=[]):
    """Wrapping the qemu system binary"""

    return cijoe.run_local(f"{cijoe.config['qemu']['system_bin']}" + " ".join(args))


def guest_init(cijoe, guest_name=None):
    """Create guest file layout"""

    if guest_name is None:
        guest_name = GUEST_NAME_DEFAULT

    guest = cijoe.config["qemu"].get(guest_name)
    guest["path"] = Path(guest["path"])

    rcode, _ = cijoe.run_local(f"mkdir -p {guest['path']}")

    return rcode


def guest_start(cijoe, guest_name=None):
    """Start a guest"""

    if guest_name is None:
        guest_name = GUEST_NAME_DEFAULT

    args = []
    args.append("-machine ")
