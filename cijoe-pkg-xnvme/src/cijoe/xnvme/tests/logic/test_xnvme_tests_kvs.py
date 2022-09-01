"""
This is a port of the tests:
xnvme_kvs_io.sh     --> test_kvs_io()

Note: the tests were named "async" did not seem to have any async be-instrumentation.
"""
import pytest

from cijoe.xnvme.tests.conftest import xnvme_device_driver as device
from cijoe.xnvme.tests.conftest import xnvme_setup


@pytest.mark.parametrize(
    "device,be_opts,cli_args",
    xnvme_setup(labels=["kvs"], opts=["be", "admin"]),
    indirect=["device"],
)
def test_kvs_io(cijoe, device, be_opts, cli_args):

    if be_opts["sync"] in ["block", "psync"]:
        pytest.skip(reason="Linux Block layer does not support simple-copy")

    err, _ = cijoe.run(f"xnvme_tests_kvs kvs_io {cli_args}")
    assert not err
