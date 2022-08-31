"""
New addition
"""
import pytest

from cijoe.xnvme.tests.conftest import xnvme_device_driver as device
from cijoe.xnvme.tests.conftest import xnvme_setup_device


@pytest.mark.parametrize(
    "device", xnvme_setup_device(labels=["file"]), indirect=["device"]
)
def test_write_fsync(cijoe, device):

    rcode, _ = cijoe.run(f"xnvme_tests_xnvme_file write-fsync {device['uri']}")
    assert not rcode


@pytest.mark.parametrize(
    "device", xnvme_setup_device(labels=["file"]), indirect=["device"]
)
def test_file_trunc(cijoe, device):

    rcode, _ = cijoe.run(f"xnvme_tests_xnvme_file file-trunc {device['uri']}")
    assert not rcode
