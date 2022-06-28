"""
    A helper-function to collecting Linux system information

    TODO
    ----

    Store the collected information as auxilary files
"""

def collect(cijoe):
    """Collect Linux system information"""

    commands = [
        ("cpuinfo", "cat /proc/cpuinfo"),
        ("memory", "free -m"),
        ("uname", "uname -a"),
        ("os-release", "cat /etc/os-release"),
        ("lshw", "lshw"),
        ("evars", "( set -o posix ; set )"),
    ]

    for label, cmd in commands:
        rcode, state = cijoe.cmd(cmd)
