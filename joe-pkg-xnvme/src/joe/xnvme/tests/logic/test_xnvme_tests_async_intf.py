import pytest

from joe.xnvme.tests.conftest import XnvmeDriver, xnvme_cli_args, xnvme_setup


@pytest.mark.parametrize(
    "device,be_opts", xnvme_setup(labels=["dev"], opts=["be", "admin", "async"])
)
def test_init_term(cijoe, device, be_opts):

    XnvmeDriver.attach(cijoe, device)
    args = xnvme_cli_args(device, be_opts)

    qdepth = 64
    for count in [1, 2, 4, 8, 16, 32, 64, 128]:
        rcode, _ = cijoe.run(
            f"xnvme_tests_async_intf init_term {args} --count {count} --qdepth {qdepth}"
        )
        assert not rcode
