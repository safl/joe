"""
This is a port of the tests:

xpy_cython_bindings_pytest.sh       --> test_cython_bindings
xpy_cython_header_pytest.sh         --> test_cython_header

"""
from pathlib import Path

import pytest

from cijoe.xnvme.tests.conftest import xnvme_device_driver as device
from cijoe.xnvme.tests.conftest import xnvme_setup

pytest.skip(allow_module_level=True, reason="Not implemented")


@pytest.mark.parametrize(
    "device,be_opts",
    xnvme_setup(labels=["dev"], opts=["be"]),
    indirect=["device"],
)
def test_cython_bindings(cijoe, device, be_opts):

    cmd = " ".join(
        [
            f"XNVME_URI={device['uri']}",
            f"XNVME_BE={be_opts['be']} ",
            f"XNVME_DEV_NSID={device['nsid']}",
            "python3 -m pytest --pyargs xnvme.cython_bindings -v -s",
        ]
    )
    err, _ = cijoe.run(cmd)
    assert not err


@pytest.mark.parametrize(
    "device,be_opts",
    xnvme_setup(labels=["dev"], opts=["be"]),
    indirect=["device"],
)
def test_cython_header(cijoe, device, be_opts):

    repos_path = (
        cijoe.config.options.get("xnvme", {}).get("repository", {}).get("path", None)
    )
    assert repos_path, "Configuration must have xnvme repository path"

    header_path = (
        Path(repos_path)
        / "python"
        / "xnvme-cy-header"
        / "xnvme"
        / "cython_header"
        / "tests"
    )
    cmd = " ".join(
        [
            f"XNVME_URI={device['uri']}",
            f"XNVME_BE={be_opts['be']} ",
            f"XNVME_DEV_NSID={device['nsid']}",
            f"python3 -m pytest --cython-collect {header_path} -v -s",
        ]
    )

    err, _ = cijoe.run(cmd)
    assert not err
