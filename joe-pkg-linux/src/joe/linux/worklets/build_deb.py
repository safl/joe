"""
    Linux Custom Kernel as Debian Package
    =====================================

    There are a myriad of ways to build and install a custom Linux kernel. This worklet
    builds it as a Debian package. The generated .deb packages are stored in
    cijoe.output_path.

    Build a custom Linux kernel using olddefconfig

    Retagetable: true
    -----------------

    Worklet arguments
    -----------------

    None
"""
from pathlib import Path


def worklet_entry(args, cijoe, step):
    """Configure, build and collect the build-artifacts"""

    repos = Path(cijoe.config.options["repository"]["path"]).resolve()
    rcode, _ = cijoe.run(f"[ -d {repos} ]")
    if rcode:
        return rcode

    localversion = "custom"

    commands = [
        "[ -f .config ] && rm .config || true",
        'yes '' | make olddefconfig',
        "./scripts/config --disable CONFIG_DEBUG_INFO",
        "./scripts/config --disable SYSTEM_TRUSTED_KEYS",
        "./scripts/config --disable SYSTEM_REVOCATION_KEYS",
        f"yes '' | make -j$(nproc) bindeb-pkg LOCALVERSION={localversion}",
        f"mkdir -p {cijoe.output_path}/artifacts",
        f"mv ../*.deb {cijoe.output_path}/artifacts/",
        f"mv ../*.changes {cijoe.output_path}/artifacts/",
        f"mv ../*.buildinfo {cijoe.output_path}/artifacts/",
    ]
    for cmd in commands:
        rcode, _ = cijoe.run(cmd, cwd=str(repos))
        if rcode:
            return rcode

    return 0
