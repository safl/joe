"""
This is a port of the tests:

xnvme_enum.sh         --> test_enum() [TODO]
xnvme_enum_fabrics.sh --> test_enum_fabrics() [TODO]
xnvme_feature_get.sh  --> test_feature_get()
xnvme_feature_set.sh  --> test_feature_set()
xnvme_format.sh       --> test_format()
xnvme_sanitize.sh     --> test_sanitize() -- TODO: Needs some investigation
xnvme_idfy.sh         --> test_idfy()
xnvme_idfy_ctrlr.sh   --> test_idfy_ctrlr()
xnvme_idfy_ns.sh      --> test_idfy_ns()
xnvme_info.sh         --> test_info()
xnvme_library_info.sh --> test_library_info()
xnvme_log-erri.sh     --> test_log_erri()
xnvme_log-health.sh   --> test_log_health()
xnvme_log.sh          --> MISSING
xnvme_padc.sh         --> test_padc()
xnvme_pioc.sh         --> test_pioc()
xnvme_sanitize.sh     --> MISSING

Observation:
    How was idfy-cs tested previously?
"""
import pytest

from cijoe.xnvme.tests.conftest import xnvme_cli_args
from cijoe.xnvme.tests.conftest import xnvme_device_driver as device
from cijoe.xnvme.tests.conftest import xnvme_setup


def test_library_info(cijoe):

    rcode, _ = cijoe.run("xnvme library-info")

    assert not rcode


def test_enum(cijoe):

    XnvmeDriver.kernel_attach(cijoe)
    rcode, _ = cijoe.run("xnvme enum")
    assert not rcode

    XnvmeDriver.kernel_detach(cijoe)
    rcode, _ = cijoe.run("xnvme enum")
    assert not rcode


@pytest.mark.parametrize(
    "device,be_opts",
    xnvme_setup(labels=["fabrics"], opts=["be"]),
    indirect=["device"],
)
def test_enum(cijoe, device, be_opts):

    rcode, _ = cijoe.run(f"xnvme enum --uri {device['uri']")

    assert not rcode


@pytest.mark.parametrize(
    "device,be_opts",
    xnvme_setup(labels=["dev"], opts=["be", "admin"]),
    indirect=["device"],
)
def test_info(cijoe, device, be_opts):

    args = xnvme_cli_args(device, be_opts)

    rcode, _ = cijoe.run(f"xnvme info {args}")

    assert not rcode


@pytest.mark.parametrize(
    "device,be_opts",
    xnvme_setup(labels=["dev"], opts=["be", "admin"]),
    indirect=["device"],
)
def test_idfy(cijoe, device, be_opts):

    args = xnvme_cli_args(device, be_opts)

    rcode, _ = cijoe.run(
        f"xnvme idfy {args} --cns 0x0 --cntid 0x0 --setid 0x0 --uuid 0x0"
    )

    assert not rcode


@pytest.mark.parametrize(
    "device,be_opts",
    xnvme_setup(labels=["dev"], opts=["be", "admin"]),
    indirect=["device"],
)
def test_idfy_ns(cijoe, device, be_opts):

    args = xnvme_cli_args(device, be_opts)

    rcode, _ = cijoe.run(f"xnvme idfy-ns {args} --nsid {device['nsid']}")

    assert not rcode


@pytest.mark.parametrize(
    "device,be_opts",
    xnvme_setup(labels=["dev"], opts=["be", "admin"]),
    indirect=["device"],
)
def test_idfy_ctrlr(cijoe, device, be_opts):

    args = xnvme_cli_args(device, be_opts)

    rcode, _ = cijoe.run(f"xnvme idfy-ctrlr {args}")

    assert not rcode


@pytest.mark.parametrize(
    "device,be_opts",
    xnvme_setup(labels=["dev"], opts=["be", "admin"]),
    indirect=["device"],
)
def test_idfy_cs(cijoe, device, be_opts):

    if be_opts["be"] == "linux" and be_opts["admin"] in ["block"]:
        pytest.skip(reason="[admin=block] does not implement idfy-cs")

    args = xnvme_cli_args(device, be_opts)

    rcode, _ = cijoe.run(f"xnvme idfy-cs {args}")

    assert not rcode


@pytest.mark.parametrize(
    "device,be_opts",
    xnvme_setup(labels=["nvm"], opts=["be", "admin"]),
    indirect=["device"],
)
def test_format(cijoe, device, be_opts):

    args = xnvme_cli_args(device, be_opts)

    rcode, _ = cijoe.run(f"xnvme format {args}")

    assert not rcode


@pytest.mark.parametrize(
    "device,be_opts",
    xnvme_setup(labels=["nvm"], opts=["be", "admin"]),
    indirect=["device"],
)
def test_format(cijoe, device, be_opts):

    pytest.skip(reason="TODO: always fails. Investigate.")

    args = xnvme_cli_args(device, be_opts)

    rcode, _ = cijoe.run(f"xnvme sanitize {args}")

    assert not rcode


@pytest.mark.parametrize(
    "device,be_opts",
    xnvme_setup(labels=["dev"], opts=["be", "admin"]),
    indirect=["device"],
)
def test_log_erri(cijoe, device, be_opts):

    if be_opts["be"] == "linux" and be_opts["admin"] in ["block"]:
        pytest.skip(reason="[admin=block] does not implement health-log")

    args = xnvme_cli_args(device, be_opts)

    rcode, _ = cijoe.run(f"xnvme log-erri {args} --nsid {device['nsid']}")

    assert not rcode


@pytest.mark.parametrize(
    "device,be_opts",
    xnvme_setup(labels=["dev"], opts=["be", "admin"]),
    indirect=["device"],
)
def test_log_health(cijoe, device, be_opts):

    if be_opts["be"] == "linux" and be_opts["admin"] in ["block"]:
        pytest.skip(reason="[admin=block] does not implement health-log")

    args = xnvme_cli_args(device, be_opts)

    # Check the controller
    rcode, _ = cijoe.run(f"xnvme log-health {args} --nsid 0xFFFFFFFF")

    # Check the namespace
    rcode, _ = cijoe.run(f"xnvme log-health {args} --nsid {device['nsid']}")

    assert not rcode


@pytest.mark.parametrize(
    "device,be_opts",
    xnvme_setup(labels=["dev"], opts=["be", "admin"]),
    indirect=["device"],
)
def test_feature_get(cijoe, device, be_opts):

    args = xnvme_cli_args(device, be_opts)

    for fid, descr in [("0x4", "Temperature threshold"), ("0x5", "Error recovery")]:
        # Get fid without setting select-bit
        rcode, _ = cijoe.run(f"xnvme feature-get {args} --fid {fid}")
        assert not rcode

        # Get fid while setting select-bit
        for sbit in ["0x0", "0x1", "0x2", "0x3"]:
            rcode, _ = cijoe.run(f"xnvme feature-get {args} --fid {fid} --sel {sbit}")
            assert not rcode


@pytest.mark.parametrize(
    "device,be_opts",
    xnvme_setup(labels=["dev"], opts=["be", "admin"]),
    indirect=["device"],
)
def test_feature_set(cijoe, device, be_opts):

    args = xnvme_cli_args(device, be_opts)

    rcode, _ = cijoe.run(f"xnvme feature-set {args} --fid 0x4 --feat 0x1 --save")

    if be_opts["admin"] == "block":
        assert rcode
    else:
        assert not rcode


@pytest.mark.parametrize(
    "device,be_opts",
    xnvme_setup(labels=["dev"], opts=["be", "admin"]),
    indirect=["device"],
)
def test_padc(cijoe, device, be_opts):
    """Construct and send an admin command (identify-controller)"""

    args = xnvme_cli_args(device, be_opts)

    opcode = "0x02"
    cns = "0x1"
    data_nbytes = 4096
    cmd_path = "/tmp/cmd-out.nvmec"

    rcode, _ = cijoe.run(f"rm {cmd_path}")

    rcode, _ = cijoe.run(
        f"nvmec create --opcode {opcode} --cdw10 {cns} --cmd-output {cmd_path}"
    )
    assert not rcode

    rcode, _ = cijoe.run(f"nvmec show --cmd-input {cmd_path}")
    assert not rcode

    rcode, _ = cijoe.run(
        f"xnvme padc {args} --cmd-input {cmd_path} --data-nbytes {data_nbytes}"
    )
    assert not rcode


@pytest.mark.parametrize(
    "device,be_opts",
    xnvme_setup(labels=["dev"], opts=["be", "admin"]),
    indirect=["device"],
)
def test_pioc(cijoe, device, be_opts):
    """Construct and send an I/O command (read)"""

    pytest.fail(reason="Not implemented")

    args = xnvme_cli_args(device, be_opts)

    opcode = "0x02"
    cns = "0x1"
    data_nbytes = 4096
    cmd_path = "/tmp/cmd-out.nvmec"

    rcode, _ = cijoe.run(f"rm {cmd_path}")

    rcode, _ = cijoe.run(
        f"nvmec create --opcode {opcode} --cdw10 {cns} --cmd-output {cmd_path}"
    )
    assert not rcode

    rcode, _ = cijoe.run(f"nvmec show --cmd-input {cmd_path}")
    assert not rcode

    rcode, _ = cijoe.run(
        f"xnvme padc {args} --cmd-input {cmd_path} --data-nbytes {data_nbytes}"
    )
    assert not rcode
