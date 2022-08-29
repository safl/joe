import pytest

from joe.xnvme.tests.conftest import xnvme_cli_args, xnvme_setup
from joe.xnvme.tests.conftest import xnvme_device_driver as device


@pytest.mark.parametrize(
    "device,be_opts",
    xnvme_setup(labels=["zns"], opts=["be", "admin", "async"]),
    indirect=["device"],
)
def test_verify(cijoe, device, be_opts):

    args = xnvme_cli_args(device, be_opts)

    rcode, _ = cijoe.run(f"xnvme_tests_znd_append verify {args}")
    assert not rcode
