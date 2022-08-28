import pytest

from joe.xnvme.tests.conftest import XnvmeDriver, xnvme_cli_args, xnvme_setup

pytest.skip(allow_module_level=True, reason="Not implemented")

#
# TODO
# * add call of selftest of ctypes
# * add "XNVME_URI=${XNVME_URI} XNVME_BE=${XNVME_BE} XNVME_DEV_NSID=${XNVME_DEV_NSID} python3 -m pytest --pyargs xnvme.cython_bindings -v -s"; then
# * add "XNVME_URI=${XNVME_URI} XNVME_BE=${XNVME_BE} XNVME_DEV_NSID=${XNVME_DEV_NSID} python3 -m pytest --cython-collect ${XNVME_REPO}/python/xnvme-cy-header/xnvme/cython_header/tests/ -v -s"; then
#


def test_xpy_dev_open(cijoe):

    rcode, _ = cijoe.run(f"xpy_enumerate")
    assert not rcode


def test_xpy_libconf(cijoe):

    rcode, _ = cijoe.run(f"xpy_libconf")
    assert not rcode


@pytest.mark.parametrize(
    "device,be_opts", xnvme_setup(labels=["dev"], opts=["be", "admin"])
)
def test_xpy_dev_open(cijoe, device, be_opts):

    XnvmeDriver.attach(cijoe, device)
    args = xnvme_cli_args(device, be_opts)

    rcode, _ = cijoe.run(f"xpy_dev_open --uri {args['uri']} --dev-nsid {args['nsid']}")
    assert not rcode
