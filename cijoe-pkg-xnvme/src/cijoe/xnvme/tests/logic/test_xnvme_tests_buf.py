"""
Although the tests has existed for a long time, it has not been added to the testcases,
it is now.
"""
import pytest

from cijoe.xnvme.tests.conftest import xnvme_cli_args
from cijoe.xnvme.tests.conftest import xnvme_device_driver as device
from cijoe.xnvme.tests.conftest import xnvme_setup


@pytest.mark.parametrize(
    "device,be_opts,cli_args",
    xnvme_setup(labels=["dev"], opts=["be"]),
    indirect=["device"],
)
def test_buf_alloc_free(cijoe, device, be_opts, cli_args):

    err, _ = cijoe.run(f"xnvme_tests_buf buf_alloc_free {cli_args} --count 31")
    assert not err


@pytest.mark.parametrize(
    "device,be_opts,cli_args",
    xnvme_setup(labels=["dev"], opts=["be"]),
    indirect=["device"],
)
def test_buf_virt_alloc_free(cijoe, device, be_opts, cli_args):

    err, _ = cijoe.run(f"xnvme_tests_buf buf_virt_alloc_free {cli_args} --count 31")
    assert not err
