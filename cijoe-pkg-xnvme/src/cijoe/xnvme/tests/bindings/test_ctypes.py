"""
This is a port of the tests:

xpy_ctypes_bin_dev_open.sh          --> test_xpy_dev_open()
xpy_ctypes_bin_enumerate.sh         --> test_xpy_enumerate()
xpy_ctypes_bin_libconf.sh           --> test_xpy_libconf()
"""
import pytest

from cijoe.xnvme.tests.conftest import xnvme_cli_args
from cijoe.xnvme.tests.conftest import xnvme_device_driver as device
from cijoe.xnvme.tests.conftest import xnvme_setup

pytest.skip(allow_module_level=True, reason="Not implemented")


def test_xpy_enumerate(cijoe):

    rcode, _ = cijoe.run("xpy_enumerate")
    assert not rcode


def test_xpy_libconf(cijoe):

    rcode, _ = cijoe.run("xpy_libconf")
    assert not rcode


@pytest.mark.parametrize(
    "device,be_opts",
    xnvme_setup(labels=["dev"], opts=["be", "admin"]),
    indirect=["device"],
)
def test_xpy_dev_open(cijoe, device, be_opts):

    args = xnvme_cli_args(device, be_opts)

    rcode, _ = cijoe.run(f"xpy_dev_open --uri {args['uri']} --dev-nsid {args['nsid']}")
    assert not rcode
