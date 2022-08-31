"""
This is a port of:

* examples-xnvme_hello.sh
"""
import pytest

from cijoe.xnvme.tests.conftest import xnvme_device_driver as device
from cijoe.xnvme.tests.conftest import xnvme_setup


@pytest.mark.parametrize(
    "device,be_opts,cli_args",
    xnvme_setup(labels=["dev"], opts=["be", "admin"]),
    indirect=["device"],
)
def test_hw(cijoe, device, be_opts, cli_args):

    rcode, _ = cijoe.run(f"xnvme_hello hw {cli_args}")
    assert not rcode
