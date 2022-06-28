"""
    kmemleak module, providing helpers to: "clear", "scan" and "cat" kmemleak

    For details on kmemleak, have a look at the Linux Kernel Documentation at

    https://www.kernel.org/doc/html/latest/dev-tools/kmemleak.html
"""


def cat(cijoe):
    """Dump the contents of kmemleak"""

    return cijoe.cmd("cat /sys/kernel/debug/kmemleak")


def scan(cijoe):
    """Scan the kernel"""

    return cijoe.cmd("echo scan > /sys/kernel/debug/kmemleak")


def clear(cijoe):
    """Clear the kmemleak"""

    return cijoe.cmd("echo clear > /sys/kernel/debug/kmemleak")
