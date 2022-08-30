import pytest

from cijoe.xnvme.tests.conftest import xnvme_cli_args
from cijoe.xnvme.tests.conftest import xnvme_device_driver as device
from cijoe.xnvme.tests.conftest import xnvme_setup

pytest.skip(allow_module_level=True, reason="Not implemented")


def test_enum(cijoe):

    rcode, _ = cijoe.run("kvs enum")
    assert not rcode

    rcode, _ = cijoe.run("kvs enum")
    assert not rcode


@pytest.mark.parametrize(
    "device,be_opts",
    xnvme_setup(labels=["kvs"], opts=["be", "admin"]),
    indirect=["device"],
)
def test_info(cijoe, device, be_opts):

    args = xnvme_cli_args(device, be_opts)

    rcode, _ = cijoe.run(f"kvs info {args}")

    assert not rcode


@pytest.mark.parametrize(
    "device,be_opts",
    xnvme_setup(labels=["kvs"], opts=["be", "admin"]),
    indirect=["device"],
)
def test_idfy_ns(cijoe, device, be_opts):

    args = xnvme_cli_args(device, be_opts)

    rcode, _ = cijoe.run(f"kvs idfy-ns {args} --nsid {device['nsid']}")

    assert not rcode


@pytest.mark.parametrize(
    "device,be_opts",
    xnvme_setup(labels=["kvs"], opts=["be", "admin"]),
    indirect=["device"],
)
def test_delete_store_exist(cijoe, device, be_opts):

    args = xnvme_cli_args(device, be_opts)

    key = "hello"
    val = "world"

    # This is just to ensure the key is not there
    cijoe.run(f"kvs delete {args} --key {key}")

    commands = [
        f"kvs exist {args} --key {key}",
        f"kvs store {args} --key {key} --value {val}",
        f"kvs exist {args} --key {key}",
    ]
    for command in commands:
        rcode, _ = cijoe.run(command)
        assert not rcode


@pytest.mark.parametrize(
    "device,be_opts",
    xnvme_setup(labels=["kvs"], opts=["be", "admin"]),
    indirect=["device"],
)
def test_delete_store_list(cijoe, device, be_opts):

    args = xnvme_cli_args(device, be_opts)

    pairs = [
        ("hello", "world"),
        ("marco", "polo"),
    ]

    # This is just to ensure the key is not there
    for key, value in pairs:
        cijoe.run(f"kvs delete {args} --key {key}")

    for key, value in pairs:
        rcode, _ = cijoe.run(f"kvs store {args} --key {key} --value {value}")
        assert not rcode

    rcode, _ = cijoe.run(f"kvs list {args} --key {key}")
    assert not rcode
