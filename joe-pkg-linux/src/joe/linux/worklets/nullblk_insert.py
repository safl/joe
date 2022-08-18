"""
    Worklet inserting nullblk with args defined in cijoe.config
"""
import joe.linux.null_blk as null_blk


def worklet_entry(args, cijoe, step):
    """Collect Linux system information"""

    rcode, _ = null_blk.insert(cijoe)

    return rcode
