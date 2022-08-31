"""
This is a port of:

* examples-xnvme_io_async_read.sh  --> test_read()
* examples-xnvme_io_async_write.sh --> test_write()
"""
import pytest

from cijoe.xnvme.tests.conftest import xnvme_device_driver as device
from cijoe.xnvme.tests.conftest import xnvme_setup


@pytest.mark.parametrize(
    "device,be_opts,cli_args",
    xnvme_setup(labels=["dev"], opts=["be", "admin", "async"]),
    indirect=["device"],
)
def test_write(cijoe, device, be_opts, cli_args):

    rcode, _ = cijoe.run(f"xnvme_io_async write {cli_args}")
    assert not rcode


@pytest.mark.parametrize(
    "device,be_opts,cli_args",
    xnvme_setup(labels=["dev"], opts=["be", "admin", "async"]),
    indirect=["device"],
)
def test_read(cijoe, device, be_opts, cli_args):

    rcode, _ = cijoe.run(f"xnvme_io_async read {cli_args}")
    assert not rcode
