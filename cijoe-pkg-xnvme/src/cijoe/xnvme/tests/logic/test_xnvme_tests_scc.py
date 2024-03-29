"""
This is a port of the tests:
xnvme_tests_scc_idfy.sh                 --> test_idfy()
xnvme_tests_scc_scopy_async.sh          --> test_scopy()
xnvme_tests_scc_scopy_sync.sh           --> test_scopy_clear()
xnvme_tests_scc_scopy_msrc_async.sh     --> test_scopy_msrc()
xnvme_tests_scc_scopy_msrc_sync.sh      --> test_scopy_msrc_clear()
xnvme_tests_scc_support.sh              --> test_support()

Note: the tests were named "async" did not seem to have any async be-instrumentation.
"""
import pytest

from cijoe.xnvme.tests.conftest import xnvme_device_driver as device
from cijoe.xnvme.tests.conftest import xnvme_setup


@pytest.mark.parametrize(
    "device,be_opts,cli_args",
    xnvme_setup(labels=["scc"], opts=["be", "admin", "sync"]),
    indirect=["device"],
)
def test_idfy(cijoe, device, be_opts, cli_args):

    if be_opts["sync"] in ["block", "psync"]:
        pytest.skip(reason="Linux Block layer does not support simple-copy")

    err, _ = cijoe.run(f"xnvme_tests_scc idfy {cli_args}")
    assert not err


@pytest.mark.parametrize(
    "device,be_opts,cli_args",
    xnvme_setup(labels=["scc"], opts=["be", "admin", "sync"]),
    indirect=["device"],
)
def test_support(cijoe, device, be_opts, cli_args):

    if be_opts["be"] == "linux" and be_opts["admin"] in ["block"]:
        pytest.skip(reason="Linux Block layer does not support simple-copy")

    err, _ = cijoe.run(f"xnvme_tests_scc support {cli_args}")
    assert not err


@pytest.mark.parametrize(
    "device,be_opts,cli_args",
    xnvme_setup(labels=["scc"], opts=["be", "admin", "sync"]),
    indirect=["device"],
)
def test_scopy(cijoe, device, be_opts, cli_args):

    if be_opts["be"] == "linux" and be_opts["admin"] in ["block"]:
        pytest.skip(reason="Linux Block layer does not support simple-copy")
    if be_opts["be"] == "linux" and be_opts["sync"] in ["block", "psync"]:
        pytest.skip(reason="Linux Block layer does not support simple-copy")

    err, _ = cijoe.run(f"xnvme_tests_scc scopy {cli_args}")
    assert not err


@pytest.mark.parametrize(
    "device,be_opts,cli_args",
    xnvme_setup(labels=["scc"], opts=["be", "admin", "sync"]),
    indirect=["device"],
)
def test_scopy_clear(cijoe, device, be_opts, cli_args):

    if be_opts["be"] == "linux" and be_opts["admin"] in ["block"]:
        pytest.skip(reason="Linux Block layer does not support simple-copy")
    if be_opts["be"] == "linux" and be_opts["sync"] in ["block", "psync"]:
        pytest.skip(reason="Linux Block layer does not support simple-copy")

    err, _ = cijoe.run(f"xnvme_tests_scc scopy {cli_args} --clear")
    assert not err


@pytest.mark.parametrize(
    "device,be_opts,cli_args",
    xnvme_setup(labels=["scc"], opts=["be", "admin", "sync"]),
    indirect=["device"],
)
def test_scopy_msrc(cijoe, device, be_opts, cli_args):

    if be_opts["be"] == "linux" and be_opts["admin"] in ["block"]:
        pytest.skip(reason="Linux Block layer does not support simple-copy")
    if be_opts["be"] == "linux" and be_opts["sync"] in ["block", "psync"]:
        pytest.skip(reason="Linux Block layer does not support simple-copy")

    err, _ = cijoe.run(f"xnvme_tests_scc scopy-msrc {cli_args}")
    assert not err


@pytest.mark.parametrize(
    "device,be_opts,cli_args",
    xnvme_setup(labels=["scc"], opts=["be", "admin", "sync"]),
    indirect=["device"],
)
def test_scopy_msrc_clear(cijoe, device, be_opts, cli_args):

    if be_opts["be"] == "linux" and be_opts["admin"] in ["block"]:
        pytest.skip(reason="Linux Block layer does not support simple-copy")
    if be_opts["be"] == "linux" and be_opts["sync"] in ["block", "psync"]:
        pytest.skip(reason="Linux Block layer does not support simple-copy")

    err, _ = cijoe.run(f"xnvme_tests_scc scopy-msrc {cli_args} --clear")
    assert not err
