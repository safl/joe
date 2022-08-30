import pytest

from cijoe.xnvme.tests.conftest import xnvme_cli_args
from cijoe.xnvme.tests.conftest import xnvme_device_driver as device
from cijoe.xnvme.tests.conftest import xnvme_setup

pytest.skip(allow_module_level=True, reason="Not implemented")

#
# TODO
# * add call of selftest of ctypes
# * add "XNVME_URI=${XNVME_URI} XNVME_BE=${XNVME_BE} XNVME_DEV_NSID=${XNVME_DEV_NSID} python3 -m pytest --pyargs xnvme.cython_bindings -v -s"; then
# * add "XNVME_URI=${XNVME_URI} XNVME_BE=${XNVME_BE} XNVME_DEV_NSID=${XNVME_DEV_NSID} python3 -m pytest --cython-collect ${XNVME_REPO}/python/xnvme-cy-header/xnvme/cython_header/tests/ -v -s"; then
#


def test_xpy_enumerate(cijoe):

    rcode, _ = cijoe.run("xpy_enumerate")
    assert not rcode


def test_xpy_libconf(cijoe):

    rcode, _ = cijoe.run("xpy_libconf")
    assert not rcode


@pytest.mark.parametrize(
    "device,be_opts",
    xnvme_setup(labels=["dev"], opts=["be", "admin"]),
    indirect=["device"],
)
def test_xpy_dev_open(cijoe, device, be_opts):

    args = xnvme_cli_args(device, be_opts)

    rcode, _ = cijoe.run(f"xpy_dev_open --uri {args['uri']} --dev-nsid {args['nsid']}")
    assert not rcode
