"""
    Worklet inserting/removing null_blk with args defined in cijoe.config

    Step arguments:

    * with.do = insert|remove
"""
import errno

import joe.linux.null_blk as null_blk


def worklet_entry(args, cijoe, step):
    """Insert or remove the null_blk"""

    do = step.get("with", {"do": "insert"}).get("do", "insert")
    if do == "insert":
        rcode, _ = null_blk.insert(cijoe)
    elif do == "remove":
        rcode, _ = null_blk.remove(cijoe)
    else:
        rcode = errno.EINVAL

    return rcode
