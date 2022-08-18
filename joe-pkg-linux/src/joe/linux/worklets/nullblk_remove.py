"""
    Worklet removing nullblk instances by unloadin the module
"""
import joe.linux.null_blk as null_blk


def worklet_entry(args, cijoe, step):
    """Collect Linux system information"""

    rcode, _ = null_blk.remove(cijoe)

    return rcode
