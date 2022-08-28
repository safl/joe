import pytest
from joe.xnvme.tests.conftest import XnvmeDriver, xnvme_cli_args, xnvme_setup


@pytest.mark.parametrize(
    "device,be_opts", xnvme_setup(labels=["dev"], opts=["be", "sync", "async", "admin"])
)
def test_verify(cijoe, device, be_opts):

    if be_opts["async"] in ["libaio"]:
        pytest.skip(reason="FIXME: [async=libaio] needs investigation")

    XnvmeDriver.attach(cijoe, device)
    args = xnvme_cli_args(device, be_opts)

    rcode, _ = cijoe.run(f"xnvme_tests_ioworker verify {args}")
    assert not rcode


@pytest.mark.parametrize(
    "device,be_opts",
    xnvme_setup(labels=["bdev"], opts=["be", "sync", "async", "admin"]),
)
@pytest.mark.skip(reason="FIXME: --direct=1 needs investigation")
def test_verify_direct(cijoe, device, be_opts):

    XnvmeDriver.attach(cijoe, device)
    args = xnvme_cli_args(device, be_opts)

    rcode, _ = cijoe.run(f"xnvme_tests_ioworker verify {args} --direct 1")
    assert not rcode
