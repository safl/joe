import pytest
from conftest import XnvmeDriver, xnvme_cli_args, xnvme_setup


@pytest.mark.parametrize(
    "device,be_opts", xnvme_setup(labels=["zrwa"], opts=["be", "admin", "sync"])
)
def test_idfy(cijoe, device, be_opts):

    XnvmeDriver.attach(cijoe, device)
    args = xnvme_cli_args(device, be_opts)

    rcode, _ = cijoe.run(f"xnvme_tests_znd_zrwa idfy {args}")
    assert not rcode


@pytest.mark.parametrize(
    "device,be_opts", xnvme_setup(labels=["zrwa"], opts=["be", "admin", "sync"])
)
def test_support(cijoe, device, be_opts):

    XnvmeDriver.attach(cijoe, device)
    args = xnvme_cli_args(device, be_opts)

    rcode, _ = cijoe.run(f"xnvme_tests_znd_zrwa support {args}")
    assert not rcode


@pytest.mark.parametrize(
    "device,be_opts", xnvme_setup(labels=["zrwa"], opts=["be", "admin", "sync"])
)
def test_open_with_zrwa(cijoe, device, be_opts):

    XnvmeDriver.attach(cijoe, device)
    args = xnvme_cli_args(device, be_opts)

    rcode, _ = cijoe.run(f"xnvme_tests_znd_zrwa open-with-zrwa {args}")
    assert not rcode


@pytest.mark.parametrize(
    "device,be_opts", xnvme_setup(labels=["zrwa"], opts=["be", "admin", "sync"])
)
def test_open_without_zrwa(cijoe, device, be_opts):

    XnvmeDriver.attach(cijoe, device)
    args = xnvme_cli_args(device, be_opts)

    rcode, _ = cijoe.run(f"xnvme_tests_znd_zrwa open-without-zrwa {args}")
    assert not rcode


@pytest.mark.parametrize(
    "device,be_opts", xnvme_setup(labels=["zrwa"], opts=["be", "admin", "sync"])
)
def test_flush(cijoe, device, be_opts):

    XnvmeDriver.attach(cijoe, device)
    args = xnvme_cli_args(device, be_opts)

    rcode, _ = cijoe.run(f"xnvme_tests_znd_zrwa flush {args}")
    assert not rcode


@pytest.mark.parametrize(
    "device,be_opts", xnvme_setup(labels=["zrwa"], opts=["be", "admin", "sync"])
)
def test_flush_explicit(cijoe, device, be_opts):

    XnvmeDriver.attach(cijoe, device)
    args = xnvme_cli_args(device, be_opts)

    rcode, _ = cijoe.run(f"xnvme_tests_znd_zrwa flush-explicit {args}")
    assert not rcode


@pytest.mark.parametrize(
    "device,be_opts", xnvme_setup(labels=["zrwa"], opts=["be", "admin", "sync"])
)
def test_flush_implicit(cijoe, device, be_opts):

    XnvmeDriver.attach(cijoe, device)
    args = xnvme_cli_args(device, be_opts)

    rcode, _ = cijoe.run(f"xnvme_tests_znd_zrwa flush-implicit {args}")
    assert not rcode
