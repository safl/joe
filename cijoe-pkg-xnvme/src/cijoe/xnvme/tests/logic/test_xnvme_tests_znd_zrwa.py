import pytest

from cijoe.xnvme.tests.conftest import xnvme_cli_args
from cijoe.xnvme.tests.conftest import xnvme_device_driver as device
from cijoe.xnvme.tests.conftest import xnvme_setup


@pytest.mark.parametrize(
    "device,be_opts",
    xnvme_setup(labels=["zrwa"], opts=["be", "admin", "sync"]),
    indirect=["device"],
)
def test_idfy(cijoe, device, be_opts):

    args = xnvme_cli_args(device, be_opts)

    rcode, _ = cijoe.run(f"xnvme_tests_znd_zrwa idfy {args}")
    assert not rcode


@pytest.mark.parametrize(
    "device,be_opts",
    xnvme_setup(labels=["zrwa"], opts=["be", "admin", "sync"]),
    indirect=["device"],
)
def test_support(cijoe, device, be_opts):

    args = xnvme_cli_args(device, be_opts)

    rcode, _ = cijoe.run(f"xnvme_tests_znd_zrwa support {args}")
    assert not rcode


@pytest.mark.parametrize(
    "device,be_opts",
    xnvme_setup(labels=["zrwa"], opts=["be", "admin", "sync"]),
    indirect=["device"],
)
def test_open_with_zrwa(cijoe, device, be_opts):

    args = xnvme_cli_args(device, be_opts)

    rcode, _ = cijoe.run(f"xnvme_tests_znd_zrwa open-with-zrwa {args}")
    assert not rcode


@pytest.mark.parametrize(
    "device,be_opts",
    xnvme_setup(labels=["zrwa"], opts=["be", "admin", "sync"]),
    indirect=["device"],
)
def test_open_without_zrwa(cijoe, device, be_opts):

    args = xnvme_cli_args(device, be_opts)

    rcode, _ = cijoe.run(f"xnvme_tests_znd_zrwa open-without-zrwa {args}")
    assert not rcode


@pytest.mark.parametrize(
    "device,be_opts",
    xnvme_setup(labels=["zrwa"], opts=["be", "admin", "sync"]),
    indirect=["device"],
)
def test_flush(cijoe, device, be_opts):

    args = xnvme_cli_args(device, be_opts)

    rcode, _ = cijoe.run(f"xnvme_tests_znd_zrwa flush {args}")
    assert not rcode


@pytest.mark.parametrize(
    "device,be_opts",
    xnvme_setup(labels=["zrwa"], opts=["be", "admin", "sync"]),
    indirect=["device"],
)
def test_flush_explicit(cijoe, device, be_opts):

    args = xnvme_cli_args(device, be_opts)

    rcode, _ = cijoe.run(f"xnvme_tests_znd_zrwa flush-explicit {args}")
    assert not rcode


@pytest.mark.parametrize(
    "device,be_opts",
    xnvme_setup(labels=["zrwa"], opts=["be", "admin", "sync"]),
    indirect=["device"],
)
def test_flush_implicit(cijoe, device, be_opts):

    args = xnvme_cli_args(device, be_opts)

    rcode, _ = cijoe.run(f"xnvme_tests_znd_zrwa flush-implicit {args}")
    assert not rcode