"""
This is a port of tests:

xnvme_tests_znd_zrwa_flush.sh               --> test_flush()
xnvme_tests_znd_zrwa_flush_explicit.sh      --> test_flush_explicit()
xnvme_tests_znd_zrwa_flush_implicit.sh      --> test_flush_implicit()
xnvme_tests_znd_zrwa_idfy.sh                --> test_idfy()
xnvme_tests_znd_zrwa_open_with_zrwa.sh      --> test_open-with_zrwa()
xnvme_tests_znd_zrwa_open_without_zrwa.sh   --> test_open_without_zrwa()
xnvme_tests_znd_zrwa_support.sh             --> test_support()
"""
import pytest

from cijoe.xnvme.tests.conftest import xnvme_device_driver as device
from cijoe.xnvme.tests.conftest import xnvme_setup


@pytest.mark.parametrize(
    "device,be_opts,cli_args",
    xnvme_setup(labels=["zrwa"], opts=["be", "admin", "sync"]),
    indirect=["device"],
)
def test_idfy(cijoe, device, be_opts, cli_args):

    err, _ = cijoe.run(f"xnvme_tests_znd_zrwa idfy {cli_args}")
    assert not err


@pytest.mark.parametrize(
    "device,be_opts,cli_args",
    xnvme_setup(labels=["zrwa"], opts=["be", "admin", "sync"]),
    indirect=["device"],
)
def test_support(cijoe, device, be_opts, cli_args):

    err, _ = cijoe.run(f"xnvme_tests_znd_zrwa support {cli_args}")
    assert not err


@pytest.mark.parametrize(
    "device,be_opts,cli_args",
    xnvme_setup(labels=["zrwa"], opts=["be", "admin", "sync"]),
    indirect=["device"],
)
def test_open_with_zrwa(cijoe, device, be_opts, cli_args):

    err, _ = cijoe.run(f"xnvme_tests_znd_zrwa open-with-zrwa {cli_args}")
    assert not err


@pytest.mark.parametrize(
    "device,be_opts,cli_args",
    xnvme_setup(labels=["zrwa"], opts=["be", "admin", "sync"]),
    indirect=["device"],
)
def test_open_without_zrwa(cijoe, device, be_opts, cli_args):

    err, _ = cijoe.run(f"xnvme_tests_znd_zrwa open-without-zrwa {cli_args}")
    assert not err


@pytest.mark.parametrize(
    "device,be_opts,cli_args",
    xnvme_setup(labels=["zrwa"], opts=["be", "admin", "sync"]),
    indirect=["device"],
)
def test_flush(cijoe, device, be_opts, cli_args):

    err, _ = cijoe.run(f"xnvme_tests_znd_zrwa flush {cli_args}")
    assert not err


@pytest.mark.parametrize(
    "device,be_opts,cli_args",
    xnvme_setup(labels=["zrwa"], opts=["be", "admin", "sync"]),
    indirect=["device"],
)
def test_flush_explicit(cijoe, device, be_opts, cli_args):

    err, _ = cijoe.run(f"xnvme_tests_znd_zrwa flush-explicit {cli_args}")
    assert not err


@pytest.mark.parametrize(
    "device,be_opts,cli_args",
    xnvme_setup(labels=["zrwa"], opts=["be", "admin", "sync"]),
    indirect=["device"],
)
def test_flush_implicit(cijoe, device, be_opts, cli_args):

    err, _ = cijoe.run(f"xnvme_tests_znd_zrwa flush-implicit {cli_args}")
    assert not err
