"""
This is a port of the tests:

xnvme_file_copy_sync.sh --> test_copy_sync()
"""
import pytest

from cijoe.xnvme.tests.conftest import xnvme_cli_args
from cijoe.xnvme.tests.conftest import xnvme_device_driver as device
from cijoe.xnvme.tests.conftest import xnvme_setup


def test_enum(cijoe):

    rcode, _ = cijoe.run("lblk enum")

    assert not rcode


@pytest.mark.parametrize(
    "device,be_opts",
    xnvme_setup(labels=["file"], opts=["be", "sync"]),
    indirect=["device"],
)
def test_copy_sync(cijoe, device, be_opts):

    src, dst, iosize = ("/tmp/input.bin", "/tmp/output.bin", 4096)

    prep = [
        f"dd if=/dev/zero of={dst} bs=1M count=1000",
        "sync",
        "free -m",
        "df -h",
        "lsblk",
        f"xnvme_file copy-sync {src} {dst} --size={iosize}",
        "free -m",
    ]
    for cmd in prep:
        rcode, _ = cijoe.run(cmd)
        assert not rcode
