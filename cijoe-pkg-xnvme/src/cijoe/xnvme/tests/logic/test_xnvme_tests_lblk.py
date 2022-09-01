"""
This is a port of the tests:

xnvme_tests_lblk_io.sh                      --> test_io()
xnvme_tests_lblk_scopy.sh                   --> test_scopy()
xnvme_tests_lblk_write_uncorrectable.sh     --> test_write_uncorrectable()
xnvme_tests_lblk_zero.sh                    --> test_write_zeroes()
"""
import pytest

from cijoe.xnvme.tests.conftest import xnvme_device_driver as device
from cijoe.xnvme.tests.conftest import xnvme_setup


@pytest.mark.parametrize(
    "device,be_opts,cli_args",
    xnvme_setup(labels=["dev"], opts=["be", "admin", "sync"]),
    indirect=["device"],
)
def test_io(cijoe, device, be_opts, cli_args):

    err, _ = cijoe.run(f"xnvme_tests_lblk io {cli_args}")
    assert not err


@pytest.mark.parametrize(
    "device,be_opts,cli_args",
    xnvme_setup(labels=["scc"], opts=["be", "admin", "sync"]),
    indirect=["device"],
)
def test_scopy(cijoe, device, be_opts, cli_args):

    if be_opts["be"] == "linux" and be_opts["sync"] in ["block", "psync"]:
        pytest.skip(reason=f"Not supported: simple-copy via { be_opts['sync'] }")

    err, _ = cijoe.run(f"xnvme_tests_lblk scopy {cli_args}")
    assert not err


@pytest.mark.parametrize(
    "device,be_opts,cli_args",
    xnvme_setup(labels=["write_uncor"], opts=["be", "admin", "sync"]),
    indirect=["device"],
)
def test_write_uncorrectable(cijoe, device, be_opts, cli_args):

    if be_opts["be"] == "linux" and be_opts["sync"] in ["block", "psync"]:
        pytest.skip(reason=f"Not supported: write_uncor via { be_opts['sync'] }")

    err, _ = cijoe.run(f"xnvme_tests_lblk write_uncorrectable {cli_args}")
    assert not err


@pytest.mark.parametrize(
    "device,be_opts,cli_args",
    xnvme_setup(labels=["write_zeroes"], opts=["be", "admin", "sync"]),
    indirect=["device"],
)
def test_write_zeroes(cijoe, device, be_opts, cli_args):

    if be_opts["be"] == "linux" and be_opts["sync"] in ["block", "psync"]:
        pytest.skip(reason=f"Not supported: write_zeroes via { be_opts['sync'] }")

    err, _ = cijoe.run(f"xnvme_tests_lblk write_zeroes {cli_args}")
    assert not err
