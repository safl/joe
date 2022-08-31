"""
This is a port of the tests:

lblk_enum.sh --> test_enum()
lblk_idfy.sh --> test_idfy()
lblk_info.sh --> test_info()
lblk_read.sh --> test_read()
lblk_write.sh --> test_write()
lblk_write_uncor.sh --> test_write_uncor()
lblk_write_zeroes.sh --> test_write_zeroes()
"""
import pytest

from cijoe.xnvme.tests.conftest import xnvme_cli_args
from cijoe.xnvme.tests.conftest import xnvme_device_driver as device
from cijoe.xnvme.tests.conftest import xnvme_setup


def test_enum(cijoe):

    rcode, _ = cijoe.run("lblk enum")

    assert not rcode


@pytest.mark.parametrize(
    "device,be_opts",
    xnvme_setup(labels=["dev"], opts=["be", "admin"]),
    indirect=["device"],
)
def test_info(cijoe, device, be_opts):

    args = xnvme_cli_args(device, be_opts)

    rcode, _ = cijoe.run(f"lblk info {args}")

    assert not rcode


@pytest.mark.parametrize(
    "device,be_opts",
    xnvme_setup(labels=["dev"], opts=["be", "admin"]),
    indirect=["device"],
)
def test_idfy(cijoe, device, be_opts):

    args = xnvme_cli_args(device, be_opts)

    rcode, _ = cijoe.run(f"lblk idfy {args}")

    assert not rcode


@pytest.mark.parametrize(
    "device,be_opts",
    xnvme_setup(labels=["dev"], opts=["be", "admin"]),
    indirect=["device"],
)
def test_read(cijoe, device, be_opts):

    args = xnvme_cli_args(device, be_opts)

    rcode, _ = cijoe.run(f"lblk read {args} --slba 0x0 --nlb 0")

    assert not rcode


@pytest.mark.parametrize(
    "device,be_opts",
    xnvme_setup(labels=["dev"], opts=["be", "admin"]),
    indirect=["device"],
)
def test_write(cijoe, device, be_opts):

    args = xnvme_cli_args(device, be_opts)

    rcode, _ = cijoe.run(f"lblk write {args} --slba 0x0 --nlb 0")

    assert not rcode


@pytest.mark.parametrize(
    "device,be_opts",
    xnvme_setup(labels=["write_uncor"], opts=["be", "admin"]),
    indirect=["device"],
)
def test_write_uncor(cijoe, device, be_opts):

    args = xnvme_cli_args(device, be_opts)

    rcode, _ = cijoe.run(f"lblk write-uncor {args} --slba 0x0 --nlb 0")

    assert not rcode


@pytest.mark.parametrize(
    "device,be_opts",
    xnvme_setup(labels=["write_zeroes"], opts=["be", "admin"]),
    indirect=["device"],
)
def test_write_zeroes(cijoe, device, be_opts):

    args = xnvme_cli_args(device, be_opts)

    rcode, _ = cijoe.run(f"lblk write-zeros {args} --slba 0x0 --nlb 0")

    assert not rcode
