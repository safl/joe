"""
This is a port of the tests:

xnvme_tests_enum_any_be_multi.sh --> test_multi_all_be()
xnvme_tests_enum_any_be_open.sh  --> test_open_all_be()
xnvme_tests_enum_multi.sh        --> test_open()
xnvme_tests_enum_open.sh         --> test_multi()
"""
import pytest

from cijoe.xnvme.tests.conftest import XnvmeDriver
from cijoe.xnvme.tests.conftest import xnvme_device_driver as device
from cijoe.xnvme.tests.conftest import xnvme_setup


@pytest.mark.parametrize(
    "device,be_opts,cli_args",
    xnvme_setup(labels=["dev"], opts=["be"]),
    indirect=["device"],
)
def test_open(cijoe, device, be_opts, cli_args):
    pytest.skip(reason="Currently not implemented, comments this out after merge.")

    err, _ = cijoe.run(f"xnvme_tests_enum open --count 4 --be {be_opts['be']}")
    assert not err


def test_open_all_be(cijoe):

    XnvmeDriver.kernel_attach(cijoe)
    err, _ = cijoe.run("xnvme_tests_enum open --count 4")
    assert not err

    XnvmeDriver.kernel_detach(cijoe)
    err, _ = cijoe.run("xnvme_tests_enum open --count 4")
    assert not err


@pytest.mark.parametrize(
    "device,be_opts,cli_args",
    xnvme_setup(labels=["dev"], opts=["be"]),
    indirect=["device"],
)
def test_multi(cijoe, device, be_opts, cli_args):
    pytest.skip(reason="Currently not implemented, comments this out after merge.")

    err, _ = cijoe.run(f"xnvme_tests_enum multi --count 4 --be {be_opts['be']}")
    assert not err


def test_multi_all_be(cijoe):

    XnvmeDriver.kernel_attach(cijoe)
    err, _ = cijoe.run("xnvme_tests_enum multi --count 4")
    assert not err

    XnvmeDriver.kernel_detach(cijoe)
    err, _ = cijoe.run("xnvme_tests_enum multi --count 4")
    assert not err
