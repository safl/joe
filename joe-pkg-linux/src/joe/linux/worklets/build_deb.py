"""
    Linux Custom Kernel as Debian Package
    =====================================

    There are a myriad of ways to build and install a custom Linux kernel. This worklet
    builds it as a Debian package.

    Build a custom Linux kernel using olddefconfig

    Retagetable: true
    -----------------

    Worklet arguments
    -----------------

    None
"""

def worklet_entry(args, cijoe, step):
    """Configure, build and collect the build-artifacts"""

    repos = Path(cijoe.config.options["repository"]["path"]).resolve()
    rcode, _ = cijoe.run(f"[ -d {repos} ]")
    if rcode:
        return rcode

    localversion = "custom"

    commands = [
        "make olddefconfig",
        "./scripts/config --disable CONFIG_DEBUG_INFO",
        "./scripts/config --disable SYSTEM_TRUSTED_KEYS",
        "./scripts/config --disable SYSTEM_REVOCATION_KEYS",
        "/usr/bin/time make -j$(nproc) bindeb-pkg",
    ]
    for cmd in commands:
        rcode, _ cijoe.run(cmd, cwd=str(repos), evars={"LOCALVERSION": localversion)
        if rcode:
            return rcode

    return 0
