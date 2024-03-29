"""
This is a port of the tests:

examples-zoned_io_sync_append.sh    --> test_append()
examples-zoned_io_sync_read.sh      --> test_read()
examples-zoned_io_sync_write.sh     --> test_write()
"""
import pytest

from cijoe.xnvme.tests.conftest import xnvme_device_driver as device
from cijoe.xnvme.tests.conftest import xnvme_setup


@pytest.mark.parametrize(
    "device,be_opts,cli_args",
    xnvme_setup(labels=["zns"], opts=["be", "admin", "sync"]),
    indirect=["device"],
)
def test_write(cijoe, device, be_opts, cli_args):

    if be_opts["be"] == "linux" and be_opts["sync"] in ["psync"]:
        pytest.skip(reason="psync(pread/write) does not support mgmt. send/receive")

    err, _ = cijoe.run(f"zoned_io_sync write {cli_args}")
    assert not err


@pytest.mark.parametrize(
    "device,be_opts,cli_args",
    xnvme_setup(labels=["zns"], opts=["be", "admin", "sync"]),
    indirect=["device"],
)
def test_append(cijoe, device, be_opts, cli_args):

    if be_opts["admin"] in ["block"]:
        pytest.skip(reason="Linux Block layer does not support append")
    if be_opts["sync"] in ["block", "psync"]:
        pytest.skip(reason="Linux Block layer does not support append")

    err, _ = cijoe.run(f"zoned_io_sync append {cli_args}")
    assert not err


@pytest.mark.parametrize(
    "device,be_opts,cli_args",
    xnvme_setup(labels=["zns"], opts=["be", "admin", "sync"]),
    indirect=["device"],
)
def test_read(cijoe, device, be_opts, cli_args):

    if be_opts["be"] == "linux" and be_opts["sync"] in ["psync"]:
        pytest.skip(reason="psync(pread/write) does not support mgmt. send/receive")

    err, _ = cijoe.run(f"zoned_io_sync read {cli_args}")
    assert not err
