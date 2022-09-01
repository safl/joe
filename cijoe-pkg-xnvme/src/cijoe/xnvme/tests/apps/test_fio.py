"""
This is a port of the tests:

xnvme_fioe.sh           --> test_fio_engine()
"""
from pathlib import Path
import pytest

from cijoe.xnvme.tests.conftest import xnvme_device_driver as device
from cijoe.xnvme.tests.conftest import xnvme_setup

from cijoe.fio.wrapper import fio_fancy


@pytest.mark.parametrize(
    "device,be_opts,cli_args",
    xnvme_setup(labels=["dev"], opts=["be", "admin", "sync", "async"]),
    indirect=["device"],
)
def test_fio_engine(cijoe, device, be_opts, cli_args, request):
    """
    The construction of the fio-invokation is done in 'cijoe.fio.wrapper.fio_fancy'
    """

    fio_output_fpath = Path(f"/tmp/fio-output.txt")

    err, _ = fio_fancy(
        cijoe, fio_output_fpath, "verify", "xnvme", device, be_opts
    )
    assert not err
