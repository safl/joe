"""
This is a port of the tests:

xnvme_tests_enum_any_be_multi.sh --> test_multi_all_be()
xnvme_tests_enum_any_be_open.sh  --> test_open_all_be()
xnvme_tests_enum_multi.sh        --> test_open()
xnvme_tests_enum_open.sh         --> test_multi()
"""
import pytest

from cijoe.xnvme.tests.conftest import XnvmeDriver, xnvme_cli_args
from cijoe.xnvme.tests.conftest import xnvme_device_driver as device
from cijoe.xnvme.tests.conftest import xnvme_setup


@pytest.mark.parametrize(
    "device,be_opts",
    xnvme_setup(labels=["dev"], opts=["be"]),
    indirect=["device"],
)
def test_open(cijoe, device, be_opts):

    rcode, _ = cijoe.run("xnvme_tests_enum open --count 4 --be {be_opts['be']}")
    assert not rcode


def test_open_all_be(cijoe):

    XnvmeDriver.kernel_attach(cijoe)
    rcode, _ = cijoe.run("xnvme_tests_enum open --count 4")
    assert not rcode

    XnvmeDriver.kernel_detach(cijoe)
    rcode, _ = cijoe.run("xnvme_tests_enum open --count 4")
    assert not rcode


@pytest.mark.parametrize(
    "device,be_opts",
    xnvme_setup(labels=["dev"], opts=["be"]),
    indirect=["device"],
)
def test_multi(cijoe, device, be_opts):

    rcode, _ = cijoe.run("xnvme_tests_enum multi --count 4 --be {be_opts['be']}")
    assert not rcode


def test_multi_all_be(cijoe):

    XnvmeDriver.kernel_attach(cijoe)
    rcode, _ = cijoe.run("xnvme_tests_enum multi --count 4")
    assert not rcode

    XnvmeDriver.kernel_detach(cijoe)
    rcode, _ = cijoe.run("xnvme_tests_enum multi --count 4")
    assert not rcode
