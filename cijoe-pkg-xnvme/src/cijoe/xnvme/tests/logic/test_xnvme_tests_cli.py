"""
New addition
"""
import pytest

from cijoe.xnvme.tests.conftest import xnvme_device_driver as device
from cijoe.xnvme.tests.conftest import xnvme_setup


def test_optional_none(cijoe):

    err, _ = cijoe.run("xnvme_tests_cli optional")
    assert not err


@pytest.mark.parametrize(
    "device,be_opts,cli_args",
    xnvme_setup(opts=["be", "mem", "sync", "async", "admin"]),
    indirect=["device"],
)
def test_optional_all(cijoe, device, be_opts, cli_args):

    err, _ = cijoe.run(
        f"xnvme_tests_cli optional "
        f"--be {be_opts['be']} "
        f"--mem {be_opts['mem']} "
        f"--sync {be_opts['sync']} "
        f"--async {be_opts['async']} "
        f"--admin {be_opts['admin']} "
    )
    assert not err
