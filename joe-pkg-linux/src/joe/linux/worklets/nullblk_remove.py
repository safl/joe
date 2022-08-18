"""
    Simple worklet collection Linux system information
"""

def worklet_entry(args, cijoe, step):
    """Collect Linux system information"""

    commands = [
        "lsb_release --all || cat /etc/os-release",
        "uname -a",
        "set",
        "lsblk",
        "lscpu",
        "lslocks",
        "lslogins",
        "lsmem",
        "lsmod",
        "lspci",
        "lsusb",
    ]

    rcode = 0
    for label, cmd in commands:
        err, state = cijoe.run(cmd)
        if err:
            rcode = err

    return rcode
