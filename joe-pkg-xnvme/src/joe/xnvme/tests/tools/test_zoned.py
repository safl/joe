import copy

import pytest

from joe.xnvme.tests.conftest import xnvme_cli_args, xnvme_setup
from joe.xnvme.tests.conftest import xnvme_device_driver


@pytest.mark.skip(reason="This is broken, hangs forever")
def test_enum(cijoe):

    rcode, _ = cijoe.run("zoned enum")

    assert not rcode


@pytest.mark.parametrize(
    "device,be_opts",
    xnvme_setup(labels=["zns"], opts=["be", "admin"]), indirect=["device"]
)
def test_info(cijoe, device, be_opts):

    args = xnvme_cli_args(device, be_opts)

    rcode, _ = cijoe.run(f"zoned info {args}")

    assert not rcode


@pytest.mark.parametrize(
    "device,be_opts",
    xnvme_setup(labels=["zns", "changes_log"], opts=["be", "admin"]),
    indirect=["device"],
)
def test_changes(cijoe, device, be_opts):

    args = xnvme_cli_args(device, be_opts)

    rcode, _ = cijoe.run(f"zoned changes {args}")

    assert not rcode


@pytest.mark.parametrize(
    "device,be_opts",
    xnvme_setup(labels=["zns"], opts=["be", "admin"]),
    indirect=["device"],
)
def test_idfy_ctrlr(cijoe, device, be_opts):

    args = xnvme_cli_args(device, be_opts)

    rcode, _ = cijoe.run(f"zoned idfy-ctrlr {args}")

    assert not rcode


@pytest.mark.parametrize(
    "device,be_opts",
    xnvme_setup(labels=["zns"], opts=["be", "admin"]),
    indirect=["device"],
)
def test_idfy_ns(cijoe, device, be_opts):

    args = xnvme_cli_args(device, be_opts)

    rcode, _ = cijoe.run(f"zoned idfy-ns {args}")

    assert not rcode


@pytest.mark.parametrize(
    "device,be_opts",
    xnvme_setup(labels=["zns"], opts=["be", "admin", "sync"]),
    indirect=["device"],
)
def test_append(cijoe, device, be_opts):

    if be_opts["be"] == "linux" and be_opts["sync"] in ["psync", "block"]:
        pytest.skip(reason="ENOSYS: sync=[psync,block] cannot do mgmt send/receive")

    admin_opts = copy.deepcopy(be_opts)
    del admin_opts["sync"]

    admin_args = xnvme_cli_args(device, admin_opts)
    args = xnvme_cli_args(device, be_opts)

    nlb = "1"
    slba = "0x0"

    rcode, _ = cijoe.run(f"zoned mgmt-reset {admin_args} --slba {slba}")
    assert not rcode

    for _ in range(3):
        rcode, _ = cijoe.run(f"zoned append {args} --slba {slba} --nlb {nlb}")
        assert not rcode


@pytest.mark.parametrize(
    "device,be_opts",
    xnvme_setup(labels=["zns"], opts=["be", "admin", "sync"]),
    indirect=["device"],
)
def test_report(cijoe, device, be_opts):

    if be_opts["be"] == "linux" and be_opts["sync"] in ["psync"]:
        pytest.skip(reason="ENOSYS: psync(pwrite/pread) cannot do mgmt send/receive")

    args = xnvme_cli_args(device, be_opts)

    rcode, _ = cijoe.run(f"zoned report {args}")

    assert not rcode


@pytest.mark.parametrize(
    "device,be_opts",
    xnvme_setup(labels=["zns"], opts=["be", "admin", "sync"]),
    indirect=["device"],
)
def test_report_limit(cijoe, device, be_opts):

    if be_opts["be"] == "linux" and be_opts["sync"] in ["psync"]:
        pytest.skip(reason="ENOSYS: psync(pwrite/pread) cannot do mgmt send/receive")

    args = xnvme_cli_args(device, be_opts)

    rcode, _ = cijoe.run(f"zoned report {args} --slba 0x0 --limit 1")

    assert not rcode


@pytest.mark.parametrize(
    "device,be_opts",
    xnvme_setup(labels=["zns"], opts=["be", "admin", "sync"]),
    indirect=["device"],
)
def test_report_single(cijoe, device, be_opts):

    if be_opts["be"] == "linux" and be_opts["sync"] in ["psync"]:
        pytest.skip(reason="ENOSYS: psync(pwrite/pread) cannot do mgmt send/receive")

    args = xnvme_cli_args(device, be_opts)

    rcode, _ = cijoe.run(f"zoned report {args} --slba 0x26400 --limit 1")

    assert not rcode


@pytest.mark.parametrize(
    "device,be_opts",
    xnvme_setup(labels=["zns"], opts=["be", "admin", "sync"]),
    indirect=["device"],
)
def test_report_some(cijoe, device, be_opts):

    if be_opts["be"] == "linux" and be_opts["sync"] in ["psync"]:
        pytest.skip(reason="ENOSYS: psync(pwrite/pread) cannot do mgmt send/receive")

    args = xnvme_cli_args(device, be_opts)

    rcode, _ = cijoe.run(f"zoned report {args} --slba 0x1dc00 --limit 10")

    assert not rcode


@pytest.mark.parametrize(
    "device,be_opts",
    xnvme_setup(labels=["zns"], opts=["be", "admin", "sync"]),
    indirect=["device"],
)
def test_read(cijoe, device, be_opts):

    if be_opts["be"] == "linux" and be_opts["sync"] in ["psync", "block"]:
        pytest.skip(reason="ENOSYS: sync=[psync,block] cannot do mgmt send/receive")

    args = xnvme_cli_args(device, be_opts)

    rcode, _ = cijoe.run(f"zoned read {args} --slba 0x0 --nlb 0")

    assert not rcode


@pytest.mark.parametrize(
    "device,be_opts",
    xnvme_setup(labels=["zns"], opts=["be", "admin", "sync"]),
    indirect=["device"],
)
def test_reset_report_write_report(cijoe, device, be_opts):

    if be_opts["be"] == "linux" and be_opts["sync"] in ["psync", "block"]:
        pytest.skip(reason="ENOSYS: sync=[psync,block] cannot do mgmt send/receive")

    args = xnvme_cli_args(device, be_opts)

    slba = "0x0"
    nlb = "0"
    limit = "0"

    rcode, _ = cijoe.run(f"zoned mgmt-reset {args} --slba {slba}")
    assert not rcode

    rcode, _ = cijoe.run(f"zoned report {args} --slba {slba} --limit {limit}")
    assert not rcode

    rcode, _ = cijoe.run(f"zoned write {args} --slba {slba} --nlb {nlb}")
    assert not rcode

    rcode, _ = cijoe.run(f"zoned report {args} --slba {slba} --limit {limit}")
    assert not rcode
