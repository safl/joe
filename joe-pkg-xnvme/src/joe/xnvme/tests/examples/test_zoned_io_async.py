import pytest
from conftest import XnvmeDriver, xnvme_cli_args, xnvme_setup


@pytest.mark.parametrize(
    "device,be_opts", xnvme_setup(labels=["zns"], opts=["be", "admin", "async"])
)
def test_write(cijoe, device, be_opts):

    XnvmeDriver.attach(cijoe, device)
    args = xnvme_cli_args(device, be_opts)

    rcode, _ = cijoe.run(f"zoned_io_async write {args}")

    assert not rcode


@pytest.mark.parametrize(
    "device,be_opts", xnvme_setup(labels=["zns"], opts=["be", "admin", "async"])
)
def test_append(cijoe, device, be_opts):

    if be_opts["be"] == "linux" and be_opts["admin"] == "block":
        pytest.skip(reason="Linux block-layer does not support append")

    if be_opts["be"] == "linux" and be_opts["async"] in ["io_uring", "libaio", "posix"]:
        pytest.skip(reason="Linux block-layer does not support append")

    XnvmeDriver.attach(cijoe, device)
    args = xnvme_cli_args(device, be_opts)

    rcode, _ = cijoe.run(f"zoned_io_async append {args}")

    assert not rcode


@pytest.mark.parametrize(
    "device,be_opts", xnvme_setup(labels=["zns"], opts=["be", "admin", "async"])
)
def test_read(cijoe, device, be_opts):

    XnvmeDriver.attach(cijoe, device)
    args = xnvme_cli_args(device, be_opts)

    rcode, _ = cijoe.run(f"zoned_io_async read {args}")

    assert not rcode
