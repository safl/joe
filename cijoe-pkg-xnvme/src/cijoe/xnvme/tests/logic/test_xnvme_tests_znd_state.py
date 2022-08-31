"""
This is a port of the tests:
xnvme_tests_znd_state.sh    --> test_transition()
"""
import pytest

from cijoe.xnvme.tests.conftest import xnvme_device_driver as device
from cijoe.xnvme.tests.conftest import xnvme_setup


@pytest.mark.parametrize(
    "device,be_opts,cli_args",
    xnvme_setup(labels=["zns"], opts=["be", "admin", "sync"]),
    indirect=["device"],
)
def test_transition(cijoe, device, be_opts, cli_args):

    if be_opts["be"] == "linux" and be_opts["sync"] in ["psync"]:
        pytest.skip(reason="Cannot do mgmt send/receive via psync")

    rcode, _ = cijoe.run(f"xnvme_tests_znd_state transition {cli_args}")
    assert not rcode
