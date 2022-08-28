import pytest

from joe.xnvme.tests.conftest import XnvmeDriver, xnvme_cli_args, xnvme_setup


def test_library_info(cijoe):

    rcode, _ = cijoe.run("xnvme library-info")

    assert not rcode


@pytest.mark.parametrize(
    "device,be_opts", xnvme_setup(labels=["dev"], opts=["be", "admin"])
)
def test_info(cijoe, device, be_opts):

    XnvmeDriver.attach(cijoe, device)
    args = xnvme_cli_args(device, be_opts)

    rcode, _ = cijoe.run(f"xnvme info {args}")

    assert not rcode


@pytest.mark.parametrize(
    "device,be_opts", xnvme_setup(labels=["dev"], opts=["be", "admin"])
)
def test_idfy(cijoe, device, be_opts):

    XnvmeDriver.attach(cijoe, device)
    args = xnvme_cli_args(device, be_opts)

    rcode, _ = cijoe.run(f"xnvme idfy {args} --cns 0x0")

    assert not rcode


@pytest.mark.parametrize(
    "device,be_opts", xnvme_setup(labels=["dev"], opts=["be", "admin"])
)
def test_idfy_ns(cijoe, device, be_opts):

    XnvmeDriver.attach(cijoe, device)
    args = xnvme_cli_args(device, be_opts)

    rcode, _ = cijoe.run(f"xnvme idfy-ns {args}")

    assert not rcode


@pytest.mark.parametrize(
    "device,be_opts", xnvme_setup(labels=["dev"], opts=["be", "admin"])
)
def test_idfy_ctrlr(cijoe, device, be_opts):

    XnvmeDriver.attach(cijoe, device)
    args = xnvme_cli_args(device, be_opts)

    rcode, _ = cijoe.run(f"xnvme idfy-ctrlr {args}")

    assert not rcode


@pytest.mark.parametrize(
    "device,be_opts", xnvme_setup(labels=["dev"], opts=["be", "admin"])
)
def test_idfy_cs(cijoe, device, be_opts):

    if be_opts["be"] == "linux" and be_opts["admin"] in ["block"]:
        pytest.skip(reason="[admin=block] does not implement idfy-cs")

    XnvmeDriver.attach(cijoe, device)
    args = xnvme_cli_args(device, be_opts)

    rcode, _ = cijoe.run(f"xnvme idfy-cs {args}")

    assert not rcode


@pytest.mark.parametrize(
    "device,be_opts", xnvme_setup(labels=["dev"], opts=["be", "admin"])
)
def test_log_erri(cijoe, device, be_opts):

    if be_opts["be"] == "linux" and be_opts["admin"] in ["block"]:
        pytest.skip(reason="[admin=block] does not implement health-log")

    XnvmeDriver.attach(cijoe, device)
    args = xnvme_cli_args(device, be_opts)

    logpath = "/tmp/xnvme_log-erri.bin"

    rcode, _ = cijoe.run(
        f"xnvme log-erri {args} --nsid {device['nsid']} --data-output {logpath}"
    )
    # cijoe.get(logpath, str(cijoe.output_path))

    assert not rcode


@pytest.mark.parametrize(
    "device,be_opts", xnvme_setup(labels=["dev"], opts=["be", "admin"])
)
def test_log_health(cijoe, device, be_opts):

    if be_opts["be"] == "linux" and be_opts["admin"] in ["block"]:
        pytest.skip(reason="[admin=block] does not implement health-log")

    XnvmeDriver.attach(cijoe, device)
    args = xnvme_cli_args(device, be_opts)

    rcode, _ = cijoe.run(f"xnvme log-health {args} --nsid {device['nsid']}")

    assert not rcode


@pytest.mark.parametrize(
    "device,be_opts", xnvme_setup(labels=["dev"], opts=["be", "admin"])
)
def test_feature_get(cijoe, device, be_opts):

    XnvmeDriver.attach(cijoe, device)
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
    "device,be_opts", xnvme_setup(labels=["dev"], opts=["be", "admin"])
)
def test_feature_set(cijoe, device, be_opts):

    XnvmeDriver.attach(cijoe, device)
    args = xnvme_cli_args(device, be_opts)

    rcode, _ = cijoe.run(f"xnvme feature-set {args} --fid 0x4 --save --feat 0x1")

    if be_opts["admin"] == "block":
        assert rcode
    else:
        assert not rcode


@pytest.mark.parametrize(
    "device,be_opts", xnvme_setup(labels=["dev"], opts=["be", "admin"])
)
def test_padc(cijoe, device, be_opts):
    """Construct and send an admin command (identify-controller)"""

    XnvmeDriver.attach(cijoe, device)
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
    "device,be_opts", xnvme_setup(labels=["dev"], opts=["be", "admin"])
)
def test_pioc(cijoe, device, be_opts):
    """Construct and send an I/O command (read)"""

    pytest.fail(reason="Not implemented")

    XnvmeDriver.attach(cijoe, device)
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
