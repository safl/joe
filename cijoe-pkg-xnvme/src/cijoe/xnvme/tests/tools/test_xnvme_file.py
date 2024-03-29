"""
This is a port of the tests:

xnvme_file_copy_sync.sh --> test_copy_sync()
"""
import pytest

from cijoe.xnvme.tests.conftest import xnvme_device_driver as device
from cijoe.xnvme.tests.conftest import xnvme_setup


@pytest.mark.parametrize(
    "device,be_opts,cli_args",
    xnvme_setup(labels=["file"], opts=["be", "sync"]),
    indirect=["device"],
)
def test_copy_sync(cijoe, device, be_opts, cli_args):

    src, dst, iosize = ("/tmp/input.bin", "/tmp/output.bin", 4096)

    prep = [
        f"dd if=/dev/zero of={src} bs=1M count=1000",
        "sync",
        "free -m",
        "df -h",
        "lsblk",
        f"xnvme_file copy-sync {src} {dst} --iosize={iosize}",
        f"cmp {src} {dst}",
        "free -m",
    ]
    for cmd in prep:
        err, _ = cijoe.run(cmd)
        assert not err
