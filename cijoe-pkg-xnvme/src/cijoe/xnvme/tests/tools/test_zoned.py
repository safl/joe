"""
This is a port of the tests:

zoned_append.sh                 --> test_append()
zoned_changes.sh                --> test_changes()
zoned_enum.sh                   --> test_enum()
zoned_idfy_ctrlr.sh             --> test_idfy_ctrlr()
zoned_idfy_ns.sh                --> test_idfy_ns()
zoned_info.sh                   --> test_info()
zoned_mgmt_open.sh              --> MISSING
zoned_read.sh                   --> test_read()
zoned_report.sh                 --> test_report_limit()
zoned_report_all.sh             --> test_report_all()
zoned_report_one.sh             --> test_report_single()
zoned_report_some.sh            --> test_report_some()
zoned_write.sh                  --> test_reset_report_write_report()
zoned_mgmt_open.sh              --> test_reset_open_report()

TODO: for some reason 'zoned enum' hangs forever. It did not use to do that!?
"""
import copy

import pytest

from cijoe.xnvme.tests.conftest import xnvme_cli_args
from cijoe.xnvme.tests.conftest import xnvme_device_driver as device
from cijoe.xnvme.tests.conftest import xnvme_setup


@pytest.mark.skip(reason="This is broken, hangs forever")
def test_enum(cijoe):

    err, _ = cijoe.run("zoned enum")
    assert not err


@pytest.mark.parametrize(
    "device,be_opts,cli_args",
    xnvme_setup(labels=["zns"], opts=["be", "admin"]),
    indirect=["device"],
)
def test_info(cijoe, device, be_opts, cli_args):

    err, _ = cijoe.run(f"zoned info {cli_args}")
    assert not err


@pytest.mark.parametrize(
    "device,be_opts,cli_args",
    xnvme_setup(labels=["zns", "changes_log"], opts=["be", "admin"]),
    indirect=["device"],
)
def test_changes(cijoe, device, be_opts, cli_args):

    err, _ = cijoe.run(f"zoned changes {cli_args}")
    assert not err


@pytest.mark.parametrize(
    "device,be_opts,cli_args",
    xnvme_setup(labels=["zns"], opts=["be", "admin"]),
    indirect=["device"],
)
def test_idfy_ctrlr(cijoe, device, be_opts, cli_args):

    err, _ = cijoe.run(f"zoned idfy-ctrlr {cli_args}")
    assert not err


@pytest.mark.parametrize(
    "device,be_opts,cli_args",
    xnvme_setup(labels=["zns"], opts=["be", "admin"]),
    indirect=["device"],
)
def test_idfy_ns(cijoe, device, be_opts, cli_args):

    err, _ = cijoe.run(f"zoned idfy-ns {cli_args}")
    assert not err


@pytest.mark.parametrize(
    "device,be_opts,cli_args",
    xnvme_setup(labels=["zns"], opts=["be", "admin", "sync"]),
    indirect=["device"],
)
def test_append(cijoe, device, be_opts, cli_args):

    if be_opts["be"] == "linux" and be_opts["sync"] in ["psync", "block"]:
        pytest.skip(reason="ENOSYS: sync=[psync,block] cannot do mgmt send/receive")

    admin_opts = copy.deepcopy(be_opts)
    del admin_opts["sync"]
    admin_args = xnvme_cli_args(device, admin_opts)

    nlb = "1"
    slba = "0x0"

    err, _ = cijoe.run(f"zoned mgmt-reset {admin_args} --slba {slba}")
    assert not err

    for _ in range(3):
        err, _ = cijoe.run(f"zoned append {cli_args} --slba {slba} --nlb {nlb}")
        assert not err


@pytest.mark.parametrize(
    "device,be_opts,cli_args",
    xnvme_setup(labels=["zns"], opts=["be", "admin", "sync"]),
    indirect=["device"],
)
def test_report_all(cijoe, device, be_opts, cli_args):

    if be_opts["be"] == "linux" and be_opts["sync"] in ["psync"]:
        pytest.skip(reason="ENOSYS: psync(pwrite/pread) cannot do mgmt send/receive")

    err, _ = cijoe.run(f"zoned report {cli_args}")
    assert not err


@pytest.mark.parametrize(
    "device,be_opts,cli_args",
    xnvme_setup(labels=["zns"], opts=["be", "admin", "sync"]),
    indirect=["device"],
)
def test_report_limit(cijoe, device, be_opts, cli_args):

    if be_opts["be"] == "linux" and be_opts["sync"] in ["psync"]:
        pytest.skip(reason="ENOSYS: psync(pwrite/pread) cannot do mgmt send/receive")

    err, _ = cijoe.run(f"zoned report {cli_args} --slba 0x0 --limit 1")
    assert not err


@pytest.mark.parametrize(
    "device,be_opts,cli_args",
    xnvme_setup(labels=["zns"], opts=["be", "admin", "sync"]),
    indirect=["device"],
)
def test_report_single(cijoe, device, be_opts, cli_args):

    if be_opts["be"] == "linux" and be_opts["sync"] in ["psync"]:
        pytest.skip(reason="ENOSYS: psync(pwrite/pread) cannot do mgmt send/receive")

    err, _ = cijoe.run(f"zoned report {cli_args} --slba 0x26400 --limit 1")
    assert not err


@pytest.mark.parametrize(
    "device,be_opts,cli_args",
    xnvme_setup(labels=["zns"], opts=["be", "admin", "sync"]),
    indirect=["device"],
)
def test_report_some(cijoe, device, be_opts, cli_args):

    if be_opts["be"] == "linux" and be_opts["sync"] in ["psync"]:
        pytest.skip(reason="ENOSYS: psync(pwrite/pread) cannot do mgmt send/receive")

    err, _ = cijoe.run(f"zoned report {cli_args} --slba 0x1dc00 --limit 10")
    assert not err


@pytest.mark.parametrize(
    "device,be_opts,cli_args",
    xnvme_setup(labels=["zns"], opts=["be", "admin", "sync"]),
    indirect=["device"],
)
def test_read(cijoe, device, be_opts, cli_args):

    if be_opts["be"] == "linux" and be_opts["sync"] in ["psync", "block"]:
        pytest.skip(reason="ENOSYS: sync=[psync,block] cannot do mgmt send/receive")

    err, _ = cijoe.run(f"zoned read {cli_args} --slba 0x0 --nlb 0")
    assert not err


@pytest.mark.parametrize(
    "device,be_opts,cli_args",
    xnvme_setup(labels=["zns"], opts=["be", "admin", "sync"]),
    indirect=["device"],
)
def test_reset_report_write_report(cijoe, device, be_opts, cli_args):

    if be_opts["be"] == "linux" and be_opts["sync"] in ["psync", "block"]:
        pytest.skip(reason="ENOSYS: sync=[psync,block] cannot do mgmt send/receive")

    slba = "0x0"
    nlb = "0"
    limit = "0"

    err, _ = cijoe.run(f"zoned mgmt-reset {cli_args} --slba {slba}")
    assert not err

    err, _ = cijoe.run(f"zoned report {cli_args} --slba {slba} --limit {limit}")
    assert not err

    err, _ = cijoe.run(f"zoned write {cli_args} --slba {slba} --nlb {nlb}")
    assert not err

    err, _ = cijoe.run(f"zoned report {cli_args} --slba {slba} --limit {limit}")
    assert not err


@pytest.mark.parametrize(
    "device,be_opts,cli_args",
    xnvme_setup(labels=["zns"], opts=["be", "admin", "sync"]),
    indirect=["device"],
)
def test_reset_open_report(cijoe, device, be_opts, cli_args):

    if be_opts["be"] == "linux" and be_opts["sync"] in ["psync", "block"]:
        pytest.skip(reason="ENOSYS: sync=[psync,block] cannot do mgmt send/receive")

    slba = "0x0"
    limit = "1"

    err, _ = cijoe.run(f"zoned mgmt-reset {cli_args} --slba {slba}")
    assert not err

    err, _ = cijoe.run(f"zoned mgmt-open {cli_args} --slba {slba}")
    assert not err

    err, _ = cijoe.run(f"zoned report {cli_args} --slba {slba} --limit {limit}")
    assert not err
