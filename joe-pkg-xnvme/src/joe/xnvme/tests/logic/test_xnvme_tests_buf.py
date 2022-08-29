import pytest

from joe.xnvme.tests.conftest import xnvme_cli_args, xnvme_setup
from joe.xnvme.tests.conftest import xnvme_device_driver as device


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
