import pytest

from joe.xnvme.tests.conftest import nvme_cli_args, xnvme_setup
from joe.xnvme.tests.conftest import xnvme_device_driver as device


@pytest.mark.parametrize(
    "device,be_opts",
    xnvme_setup(labels=["zns"], opts=["be", "admin", "sync"]),
    indirect=["device"],
)
def test_transition(cijoe, device, be_opts):

    if be_opts["be"] == "linux" and be_opts["sync"] in ["psync"]:
        pytest.skip(reason="Cannot do mgmt send/receive via psync")

    args = xnvme_cli_args(device, be_opts)

    rcode, _ = cijoe.run(f"xnvme_tests_znd_state transition {args}")
    assert not rcode
