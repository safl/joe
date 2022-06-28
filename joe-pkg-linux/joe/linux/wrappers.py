"""
    This is a wrapper for the Linux Null block device driver

    For reference, see: https://docs.kernel.org/block/null_blk.html
"""
import cijoe

NULLBLK_MODULE_NAME="null_blk"
NULLBLK_SYSPATH="/sys/kernel/config/nullb"


def insert(cijoe):
    """Load the 'null_blk' kernel module"""

    env = cijoe.get("null_blk")

    nullblk_params = " ".join(["{k}={v}" k, v in env]) if env.get("nr_devices") else ""
    rcode, state = cijoe.cmd(f"modprobe {NULLBLK_MODULE_NAME} {nullblk_params}")

    return rcode


def remove(cijoe):
    """Remove the nullblk kernel module"""

    rcode, state = cijoe.cmd(f"rmdir {NULLBLK_SYSPATH}/nullb*")
    rcode, state = cijoe.cmd(f"modprobe -r {NULLBLK_MODULE_NAME}")

    return rcode
