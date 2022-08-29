import pytest

from joe.xnvme.tests.conftest import xnvme_cli_args, xnvme_setup
from joe.xnvme.tests.conftest import xnvme_device_driver as device


@pytest.mark.parametrize(
    "device,be_opts",
    xnvme_setup(labels=["scc"], opts=["be", "admin", "sync"]),
    indirect=["device"],
)
def test_idfy(cijoe, device, be_opts):

    if be_opts["sync"] in ["block", "psync"]:
        pytest.skip(reason="Linux Block layer does not support simple-copy")

    args = xnvme_cli_args(device, be_opts)

    rcode, _ = cijoe.run(f"xnvme_tests_scc idfy {args}")
    assert not rcode


@pytest.mark.parametrize(
    "device,be_opts",
    xnvme_setup(labels=["scc"], opts=["be", "admin", "sync"]),
    indirect=["device"],
)
def test_scopy(cijoe, device, be_opts):

    if be_opts["be"] == "linux" and be_opts["admin"] in ["block"]:
        pytest.skip(reason="Linux Block layer does not support simple-copy")
    if be_opts["be"] == "linux" and be_opts["sync"] in ["block", "psync"]:
        pytest.skip(reason="Linux Block layer does not support simple-copy")

    args = xnvme_cli_args(device, be_opts)

    rcode, _ = cijoe.run(f"xnvme_tests_scc scopy {args}")
    assert not rcode


@pytest.mark.parametrize(
    "device,be_opts",
    xnvme_setup(labels=["scc"], opts=["be", "admin", "sync"]),
    indirect=["device"],
)
def test_scopy_clear(cijoe, device, be_opts):

    if be_opts["be"] == "linux" and be_opts["admin"] in ["block"]:
        pytest.skip(reason="Linux Block layer does not support simple-copy")
    if be_opts["be"] == "linux" and be_opts["sync"] in ["block", "psync"]:
        pytest.skip(reason="Linux Block layer does not support simple-copy")

    args = xnvme_cli_args(device, be_opts)

    rcode, _ = cijoe.run(f"xnvme_tests_scc scopy {args} --clear")
    assert not rcode


@pytest.mark.parametrize(
    "device,be_opts",
    xnvme_setup(labels=["scc"], opts=["be", "admin", "sync"]),
    indirect=["device"],
)
def test_scopy_msrc(cijoe, device, be_opts):

    if be_opts["be"] == "linux" and be_opts["admin"] in ["block"]:
        pytest.skip(reason="Linux Block layer does not support simple-copy")
    if be_opts["be"] == "linux" and be_opts["sync"] in ["block", "psync"]:
        pytest.skip(reason="Linux Block layer does not support simple-copy")

    args = xnvme_cli_args(device, be_opts)

    rcode, _ = cijoe.run(f"xnvme_tests_scc scopy-msrc {args}")
    assert not rcode


@pytest.mark.parametrize(
    "device,be_opts",
    xnvme_setup(labels=["scc"], opts=["be", "admin", "sync"]),
    indirect=["device"],
)
def test_scopy_msrc_clear(cijoe, device, be_opts):

    if be_opts["be"] == "linux" and be_opts["admin"] in ["block"]:
        pytest.skip(reason="Linux Block layer does not support simple-copy")
    if be_opts["be"] == "linux" and be_opts["sync"] in ["block", "psync"]:
        pytest.skip(reason="Linux Block layer does not support simple-copy")

    args = xnvme_cli_args(device, be_opts)

    rcode, _ = cijoe.run(f"xnvme_tests_scc scopy-msrc {args} --clear")
    assert not rcode


@pytest.mark.parametrize(
    "device,be_opts",
    xnvme_setup(labels=["scc"], opts=["be", "admin", "sync"]),
    indirect=["device"],
)
def test_support(cijoe, device, be_opts):

    if be_opts["be"] == "linux" and be_opts["admin"] in ["block"]:
        pytest.skip(reason="Linux Block layer does not support simple-copy")

    args = xnvme_cli_args(device, be_opts)

    rcode, _ = cijoe.run(f"xnvme_tests_scc support {args}")
    assert not rcode
