"""
New addition
"""
import pytest

from cijoe.xnvme.tests.conftest import xnvme_cli_args
from cijoe.xnvme.tests.conftest import xnvme_device_driver as device
from cijoe.xnvme.tests.conftest import xnvme_setup


def test_optional_none(cijoe):

    rcode, _ = cijoe.run("xnvme_tests_cli optional")
    assert not rcode


@pytest.mark.parametrize(
    "device,be_opts",
    xnvme_setup(opts=["be", "mem", "sync", "async", "admin"]),
    indirect=["device"],
)
def test_optional_all(cijoe, device, be_opts):

    args = xnvme_cli_args({}, be_opts)

    rcode, _ = cijoe.run(f"xnvme_tests_cli optional {args}")
    assert not rcode
