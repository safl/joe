"""
This is a port of the tests:

xnvme_tests_znd_append.sh --> test_verify
"""
import pytest

from cijoe.xnvme.tests.conftest import xnvme_device_driver as device
from cijoe.xnvme.tests.conftest import xnvme_setup


@pytest.mark.parametrize(
    "device,be_opts,cli_args",
    xnvme_setup(labels=["zns"], opts=["be", "admin", "async"]),
    indirect=["device"],
)
def test_verify(cijoe, device, be_opts, cli_args):

    err, _ = cijoe.run(f"xnvme_tests_znd_append verify {cli_args}")
    assert not err
