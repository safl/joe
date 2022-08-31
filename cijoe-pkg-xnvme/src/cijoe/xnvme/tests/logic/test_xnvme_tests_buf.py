"""
Although the tests has existed for a long time, it has not been added to the testcases,
it is now.
"""
import pytest

from cijoe.xnvme.tests.conftest import xnvme_cli_args
from cijoe.xnvme.tests.conftest import xnvme_device_driver as device
from cijoe.xnvme.tests.conftest import xnvme_setup


@pytest.mark.parametrize(
    "device,be_opts", xnvme_setup(labels=["dev"], opts=["be"]), indirect=["device"]
)
def test_buf_alloc_free(cijoe, device, be_opts):

    args = xnvme_cli_args(device, be_opts)

    rcode, _ = cijoe.run(f"xnvme_tests_buf buf_alloc_free {args} --count 31")
    assert not rcode


@pytest.mark.parametrize(
    "device,be_opts", xnvme_setup(labels=["dev"], opts=["be"]), indirect=["device"]
)
def test_buf_virt_alloc_free(cijoe, device, be_opts):

    args = xnvme_cli_args(device, be_opts)

    rcode, _ = cijoe.run(f"xnvme_tests_buf buf_virt_alloc_free {args} --count 31")
    assert not rcode
