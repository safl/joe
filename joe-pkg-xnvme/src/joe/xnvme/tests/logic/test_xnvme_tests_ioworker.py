import pytest

from joe.xnvme.tests.conftest import xnvme_cli_args, xnvme_setup
from joe.xnvme.tests.conftest import xnvme_device_driver as device


@pytest.mark.parametrize(
    "device,be_opts",
    xnvme_setup(labels=["dev"], opts=["be", "sync", "async", "admin"]),
    indirect=["device"],
)
def test_verify(cijoe, device, be_opts):

    if be_opts["async"] in ["libaio"]:
        pytest.skip(reason="FIXME: [async=libaio] needs investigation")

    args = xnvme_cli_args(device, be_opts)

    rcode, _ = cijoe.run(f"xnvme_tests_ioworker verify {args}")
    assert not rcode


@pytest.mark.parametrize(
    "device,be_opts",
    xnvme_setup(labels=["bdev"], opts=["be", "sync", "async", "admin"]),
    indirect=["device"],
)
@pytest.mark.skip(reason="FIXME: --direct=1 needs investigation")
def test_verify_direct(cijoe, device, be_opts):

    args = xnvme_cli_args(device, be_opts)

    rcode, _ = cijoe.run(f"xnvme_tests_ioworker verify {args} --direct 1")
    assert not rcode
