"""
This is a port of the tests:

examples-zoned_io_async_append.sh   --> test_append()
examples-zoned_io_async_read.sh     --> test_read()
examples-zoned_io_async_write.sh    --> test_write()

"""
import pytest

from cijoe.xnvme.tests.conftest import xnvme_device_driver as device
from cijoe.xnvme.tests.conftest import xnvme_setup


@pytest.mark.parametrize(
    "device,be_opts,cli_args",
    xnvme_setup(labels=["zns"], opts=["be", "admin", "async"]),
    indirect=["device"],
)
def test_write(cijoe, device, be_opts, cli_args):

    rcode, _ = cijoe.run(f"zoned_io_async write {cli_args}")
    assert not rcode


@pytest.mark.parametrize(
    "device,be_opts,cli_args",
    xnvme_setup(labels=["zns"], opts=["be", "admin", "async"]),
    indirect=["device"],
)
def test_append(cijoe, device, be_opts, cli_args):

    if be_opts["be"] == "linux" and be_opts["admin"] == "block":
        pytest.skip(reason="Linux block-layer does not support append")

    if be_opts["be"] == "linux" and be_opts["async"] in ["io_uring", "libaio", "posix"]:
        pytest.skip(reason="Linux block-layer does not support append")

    rcode, _ = cijoe.run(f"zoned_io_async append {cli_args}")
    assert not rcode


@pytest.mark.parametrize(
    "device,be_opts,cli_args",
    xnvme_setup(labels=["zns"], opts=["be", "admin", "async"]),
    indirect=["device"],
)
def test_read(cijoe, device, be_opts, cli_args):

    rcode, _ = cijoe.run(f"zoned_io_async read {cli_args}")
    assert not rcode
