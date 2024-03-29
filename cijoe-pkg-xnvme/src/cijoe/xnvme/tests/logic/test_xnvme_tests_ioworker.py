"""
New addition
"""
import pytest

from cijoe.xnvme.tests.conftest import xnvme_device_driver as device
from cijoe.xnvme.tests.conftest import xnvme_setup


@pytest.mark.parametrize(
    "device,be_opts,cli_args",
    xnvme_setup(labels=["dev"], opts=["be", "sync", "async", "admin"]),
    indirect=["device"],
)
def test_verify(cijoe, device, be_opts, cli_args):

    if be_opts["async"] in ["libaio"]:
        pytest.skip(reason="FIXME: [async=libaio] needs investigation")

    err, _ = cijoe.run(f"xnvme_tests_ioworker verify {cli_args}")
    assert not err


@pytest.mark.parametrize(
    "device,be_opts,cli_args",
    xnvme_setup(labels=["bdev"], opts=["be", "sync", "async", "admin"]),
    indirect=["device"],
)
@pytest.mark.skip(reason="FIXME: --direct=1 needs investigation")
def test_verify_direct(cijoe, device, be_opts, cli_args):

    err, _ = cijoe.run(f"xnvme_tests_ioworker verify {cli_args} --direct 1")
    assert not err
