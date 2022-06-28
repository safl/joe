"""
    This is a wrapper for the Linux Null block device driver

    To use it, one must have permissions to modprobe,rmmod and modify the /syscfg

    For reference, see: https://docs.kernel.org/block/null_blk.html
"""
NULLBLK_MODULE_NAME = "null_blk"
NULLBLK_SYSPATH = "/sys/kernel/config/nullb"


def insert(cijoe, env=None):
    """Load the 'null_blk' kernel module using parameters defined in the env"""

    if env is None:
        env = cijoe.get_env("null_blk")

    nullblk_params = (
        " ".join([f"{k}={v}" for k, v in env.items()]) if env.get("nr_devices") else ""
    )
    rcode, state = cijoe.cmd(f"modprobe {NULLBLK_MODULE_NAME} {nullblk_params}")

    return rcode


def remove(cijoe):
    """Remove the null_blk kernel module"""

    rcode, state = cijoe.cmd(f"rmdir {NULLBLK_SYSPATH}/nullb*")
    rcode, state = cijoe.cmd(f"modprobe -r {NULLBLK_MODULE_NAME}")

    return rcode
