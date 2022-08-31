"""
This is a port of the tests:
xnvme_kvs_io.sh     --> test_kvs_io()

Note: the tests were named "async" did not seem to have any async be-instrumentation.
"""
import pytest

from cijoe.xnvme.tests.conftest import xnvme_cli_args
from cijoe.xnvme.tests.conftest import xnvme_device_driver as device
from cijoe.xnvme.tests.conftest import xnvme_setup


@pytest.mark.parametrize(
    "device,be_opts",
    xnvme_setup(labels=["kvs"], opts=["be", "admin"]),
    indirect=["device"],
)
def test_kvs_io(cijoe, device, be_opts):

    if be_opts["sync"] in ["block", "psync"]:
        pytest.skip(reason="Linux Block layer does not support simple-copy")

    args = xnvme_cli_args(device, be_opts)

    rcode, _ = cijoe.run(f"xnvme_tests_kvs kvs_io {args}")
    assert not rcode
