import os

import pytest

backends = [
    "linux": {
        "async": ["emu", "thrpool", "aio", "libaio", "io_uring", "io_uring_cmd"],
        "sync": ["nvme", "psync"],
        "admin": ["nvme", "block"]
    },
    "spdk": {
        "async": ["nvme"],
        "sync": ["nvme"],
        "admin": ["nvme"],
    }
]

def test_cli_xnvme_list(cijoe):

    rcode, state = cijoe.run("xnvme list")
    assert not rcode, os.path.join(cijoe.output_path, cijoe.output_ident, "cmd.log")


def test_cli_xnvme_enum(cijoe):

    rcode, state = cijoe.run("xnvme enum")
    assert not rcode, os.path.join(cijoe.output_path, cijoe.output_ident, "cmd.log")


@pytest.mark.parametrize("xnvme_config", xnvme_configs)
def test_cli_xnvme_info(cijoe, nvme, xnvme_config):

    if not nvme:
        pytest.skip()

    rcode, state = cijoe.run(f"xnvme info {nvme['bdev']}")
    assert not rcode, os.path.join(cijoe.output_path, cijoe.output_ident, "cmd.log")


def test_cli_xnvme_library_info(cijoe):

    rcode, state = cijoe.run("xnvme library-info")
    assert not rcode, os.path.join(cijoe.output_path, cijoe.output_ident, "cmd.log")
