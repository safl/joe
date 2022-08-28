import pytest
from joe.xnvme.tests.conftest import XnvmeDriver, xnvme_cli_args, xnvme_setup_device


@pytest.mark.parametrize("device", xnvme_setup_device(labels=["file"]))
def test_write_fsync(cijoe, device):

    XnvmeDriver.attach(cijoe, device)

    rcode, _ = cijoe.run(f"xnvme_tests_xnvme_file write-fsync {device['uri']}")
    assert not rcode


@pytest.mark.parametrize("device", xnvme_setup_device(labels=["file"]))
def test_file_trunc(cijoe, device):

    XnvmeDriver.attach(cijoe, device)

    rcode, _ = cijoe.run(f"xnvme_tests_xnvme_file file-trunc {device['uri']}")
    assert not rcode
