import pytest
from conftest import XnvmeDriver, xnvme_cli_args, xnvme_setup


def test_enum(cijoe):

    rcode, _ = cijoe.run(f"lblk enum")

    assert not rcode


@pytest.mark.parametrize(
    "device,be_opts", xnvme_setup(labels=["dev"], opts=["be", "admin"])
)
def test_info(cijoe, device, be_opts):

    XnvmeDriver.attach(cijoe, device)
    args = xnvme_cli_args(device, be_opts)

    rcode, _ = cijoe.run(f"lblk info {args}")

    assert not rcode


@pytest.mark.parametrize(
    "device,be_opts", xnvme_setup(labels=["dev"], opts=["be", "admin"])
)
def test_idfy(cijoe, device, be_opts):

    XnvmeDriver.attach(cijoe, device)
    args = xnvme_cli_args(device, be_opts)

    rcode, _ = cijoe.run(f"lblk idfy {args}")

    assert not rcode


@pytest.mark.parametrize(
    "device,be_opts", xnvme_setup(labels=["dev"], opts=["be", "admin"])
)
def test_read(cijoe, device, be_opts):

    XnvmeDriver.attach(cijoe, device)
    args = xnvme_cli_args(device, be_opts)

    rcode, _ = cijoe.run(f"lblk read {args} --slba 0x0 --nlb 0")

    assert not rcode


@pytest.mark.parametrize(
    "device,be_opts", xnvme_setup(labels=["dev"], opts=["be", "admin"])
)
def test_write(cijoe, device, be_opts):

    XnvmeDriver.attach(cijoe, device)
    args = xnvme_cli_args(device, be_opts)

    rcode, _ = cijoe.run(f"lblk write {args} --slba 0x0 --nlb 0")

    assert not rcode


@pytest.mark.parametrize(
    "device,be_opts", xnvme_setup(labels=["write_uncor"], opts=["be", "admin"])
)
def test_write_uncor(cijoe, device, be_opts):

    XnvmeDriver.attach(cijoe, device)
    args = xnvme_cli_args(device, be_opts)

    rcode, _ = cijoe.run(f"lblk write-uncor {args} --slba 0x0 --nlb 0")

    assert not rcode


@pytest.mark.parametrize(
    "device,be_opts", xnvme_setup(labels=["write_zeroes"], opts=["be", "admin"])
)
def test_write_zeroes(cijoe, device, be_opts):

    XnvmeDriver.attach(cijoe, device)
    args = xnvme_cli_args(device, be_opts)

    rcode, _ = cijoe.run(f"lblk write-zeros {args} --slba 0x0 --nlb 0")

    assert not rcode
