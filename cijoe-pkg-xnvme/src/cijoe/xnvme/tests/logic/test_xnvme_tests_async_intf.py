"""
This is a port of the tests:

xnvme_tests_async_intf01.sh     --> test_init_term()
xnvme_tests_async_intf02.sh     --> test_init_term()
xnvme_tests_async_intf03.sh     --> test_init_term()
xnvme_tests_async_intf04.sh     --> test_init_term()

The difference of the above tests are the variance of the parameter --count.
The first three had hard-coded 1... 4 ... 8.
The last looped over the sequence [1, ..., 128]

The first three are redundant as the general form catches all.
Thus, just implementing that. Also, this happended due to issue previously. Now, it just
serves as a regression-test, and might as well catch all in one.
"""
import pytest

from cijoe.xnvme.tests.conftest import xnvme_cli_args
from cijoe.xnvme.tests.conftest import xnvme_device_driver as device
from cijoe.xnvme.tests.conftest import xnvme_setup


@pytest.mark.parametrize(
    "device,be_opts",
    xnvme_setup(labels=["dev"], opts=["be", "admin", "async"]),
    indirect=["device"],
)
def test_init_term(cijoe, device, be_opts):

    args = xnvme_cli_args(device, be_opts)

    qdepth = 64
    for count in [1, 2, 4, 8, 16, 32, 64, 128]:
        rcode, _ = cijoe.run(
            f"xnvme_tests_async_intf init_term {args} --count {count} --qdepth {qdepth}"
        )
        assert not rcode
