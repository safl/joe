import pytest
from joe.xnvme.tests.conftest import XnvmeDriver, xnvme_cli_args, xnvme_setup


def test_open(cijoe):

    XnvmeDriver.kernel_attach(cijoe)
    rcode, _ = cijoe.run(f"xnvme_tests_enum open --count 4")
    assert not rcode

    XnvmeDriver.kernel_detach(cijoe)
    rcode, _ = cijoe.run(f"xnvme_tests_enum open --count 4")
    assert not rcode


def test_multi(cijoe):

    XnvmeDriver.kernel_attach(cijoe)
    rcode, _ = cijoe.run(f"xnvme_tests_enum multi --count 4")
    assert not rcode

    XnvmeDriver.kernel_detach(cijoe)
    rcode, _ = cijoe.run(f"xnvme_tests_enum multi --count 4")
    assert not rcode
