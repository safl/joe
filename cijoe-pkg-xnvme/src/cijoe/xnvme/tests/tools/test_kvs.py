"""
This is a port of the tests:

xnvme_kvs_enum.sh       --> test_enum
xnvme_kvs_exist.sh     --> test_delete_store_exist()
xnvme_kvs_idfy_ns.sh   --> test_idfy_ns()
xnvme_kvs_list.sh      --> test_delete_store_list()
xnvme_kvs_retrieve.sh  --> test_retrieve()
xnvme_kvs_store_opt.sh --> test_store_optional()

Note
----

Currently no upstream support for the KVS command-set, thus these tests are skipped
"""
import pytest

from cijoe.xnvme.tests.conftest import XnvmeDriver
from cijoe.xnvme.tests.conftest import xnvme_device_driver as device
from cijoe.xnvme.tests.conftest import xnvme_setup

pytest.skip(allow_module_level=True, reason="Not implemented")


def test_enum(cijoe):

    XnvmeDriver.kernel_attach(cijoe)
    err, _ = cijoe.run("kvs enum")
    assert not err

    XnvmeDriver.kernel_detach(cijoe)
    err, _ = cijoe.run("kvs enum")
    assert not err


@pytest.mark.parametrize(
    "device,be_opts,cli_args",
    xnvme_setup(labels=["kvs"], opts=["be", "admin"]),
    indirect=["device"],
)
def test_info(cijoe, device, be_opts, cli_args):

    err, _ = cijoe.run(f"kvs info {cli_args}")
    assert not err


@pytest.mark.parametrize(
    "device,be_opts,cli_args",
    xnvme_setup(labels=["kvs"], opts=["be", "admin"]),
    indirect=["device"],
)
def test_idfy_ns(cijoe, device, be_opts, cli_args):

    err, _ = cijoe.run(f"kvs idfy-ns {cli_args} --nsid {device['nsid']}")
    assert not err


@pytest.mark.parametrize(
    "device,be_opts,cli_args",
    xnvme_setup(labels=["kvs"], opts=["be", "admin"]),
    indirect=["device"],
)
def test_delete_store_exist(cijoe, device, be_opts, cli_args):

    key = "hello"
    val = "world"

    # This is just to ensure the key is not there
    cijoe.run(f"kvs delete {cli_args} --key {key}")

    commands = [
        f"kvs exist {cli_args} --key {key}",
        f"kvs store {cli_args} --key {key} --value {val}",
        f"kvs exist {cli_args} --key {key}",
    ]
    for command in commands:
        err, _ = cijoe.run(command)
        assert not err


@pytest.mark.parametrize(
    "device,be_opts,cli_args",
    xnvme_setup(labels=["kvs"], opts=["be", "admin"]),
    indirect=["device"],
)
def test_delete_store_list(cijoe, device, be_opts, cli_args):

    pairs = [
        ("hello", "world"),
        ("marco", "polo"),
    ]

    # This is just to ensure the key is not there
    for key, value in pairs:
        cijoe.run(f"kvs delete {cli_args} --key {key}")

    for key, value in pairs:
        err, _ = cijoe.run(f"kvs store {cli_args} --key {key} --value {value}")
        assert not err

    err, _ = cijoe.run(f"kvs list {cli_args} --key {key}")
    assert not err


@pytest.mark.parametrize(
    "device,be_opts,cli_args",
    xnvme_setup(labels=["kvs"], opts=["be", "admin"]),
    indirect=["device"],
)
def test_retrieve(cijoe, device, be_opts, cli_args):

    key, val = ("hello", "world")

    # This is just to ensure the key is not there
    cijoe.run(f"kvs delete {cli_args} --key {key}")

    err, _ = cijoe.run(f"kvs retrieve {cli_args} --key {key}")
    assert not err

    err, _ = cijoe.run(f"kvs store {cli_args} --key {key} --value {val}")
    assert not err

    err, _ = cijoe.run(f"kvs retrieve {cli_args} --key {key}")
    assert not err


@pytest.mark.parametrize(
    "device,be_opts,cli_args",
    xnvme_setup(labels=["kvs"], opts=["be", "admin"]),
    indirect=["device"],
)
def test_store_optional(cijoe, device, be_opts, cli_args):

    key = "hello"
    val = "world"
    val_next = "xnvme"

    err, _ = cijoe.run(f"kvs delete {cli_args} --key {key}")

    err, _ = cijoe.run(f"kvs store {cli_args} --key {key} --value {val} --only-update")
    assert not err

    err, _ = cijoe.run(f"kvs store {cli_args} --key {key} --value {val}")
    assert not err

    err, _ = cijoe.run(
        f"kvs store {cli_args} --key {key} --value {val_next} --only-update"
    )
    assert not err

    err, _ = cijoe.run(f"kvs store {cli_args} --key {key} --value {val} --only-add")
    assert err

    err, _ = cijoe.run(f"kvs delete {cli_args} --key {key}")
    assert not err

    err, _ = cijoe.run(f"kvs store {cli_args} --key {key} --value {val} --only-add")
    assert not err
