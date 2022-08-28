import pytest

from joe.xnvme.tests.conftest import XnvmeDriver, xnvme_cli_args, xnvme_setup


@pytest.mark.parametrize(
    "device,be_opts", xnvme_setup(labels=["dev"], opts=["be", "admin", "sync"])
)
def test_io(cijoe, device, be_opts):

    XnvmeDriver.attach(cijoe, device)
    args = xnvme_cli_args(device, be_opts)

    rcode, _ = cijoe.run(f"xnvme_tests_lblk io {args}")
    assert not rcode


@pytest.mark.parametrize(
    "device,be_opts", xnvme_setup(labels=["scc"], opts=["be", "admin", "sync"])
)
def test_scopy(cijoe, device, be_opts):

    if be_opts["be"] == "linux" and be_opts["sync"] in ["block", "psync"]:
        pytest.skip(reason=f"Not supported: simple-copy via { be_opts['sync'] }")

    XnvmeDriver.attach(cijoe, device)
    args = xnvme_cli_args(device, be_opts)

    rcode, _ = cijoe.run(f"xnvme_tests_lblk scopy {args}")
    assert not rcode


@pytest.mark.parametrize(
    "device,be_opts", xnvme_setup(labels=["write_uncor"], opts=["be", "admin", "sync"])
)
def test_write_uncorrectable(cijoe, device, be_opts):

    if be_opts["be"] == "linux" and be_opts["sync"] in ["block", "psync"]:
        pytest.skip(reason=f"Not supported: write_uncor via { be_opts['sync'] }")

    XnvmeDriver.attach(cijoe, device)
    args = xnvme_cli_args(device, be_opts)

    rcode, _ = cijoe.run(f"xnvme_tests_lblk write_uncorrectable {args}")
    assert not rcode


@pytest.mark.parametrize(
    "device,be_opts", xnvme_setup(labels=["write_zeroes"], opts=["be", "admin", "sync"])
)
def test_write_zeroes(cijoe, device, be_opts):

    if be_opts["be"] == "linux" and be_opts["sync"] in ["block", "psync"]:
        pytest.skip(reason=f"Not supported: write_zeroes via { be_opts['sync'] }")

    XnvmeDriver.attach(cijoe, device)
    args = xnvme_cli_args(device, be_opts)

    rcode, _ = cijoe.run(f"xnvme_tests_lblk write_zeroes {args}")
    assert not rcode
