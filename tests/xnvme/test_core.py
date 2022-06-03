import os

import pytest


def test_cli_xnvme_list(cijoe):

    rcode, state = cijoe.cmd("xnvme list")
    assert not rcode, os.path.join(cijoe.output_path, cijoe.output_ident, "cmd.log")


def test_cli_xnvme_enum(cijoe):

    rcode, state = cijoe.cmd("xnvme enum")
    assert not rcode, os.path.join(cijoe.output_path, cijoe.output_ident, "cmd.log")


def test_cli_xnvme_info(cijoe, nvme):

    if not nvme:
        pytest.skip()

    rcode, state = cijoe.cmd(f"xnvme info {nvme['bdev']}")
    assert not rcode, os.path.join(cijoe.output_path, cijoe.output_ident, "cmd.log")


def test_cli_xnvme_library_info(cijoe):

    rcode, state = cijoe.cmd("xnvme library-info")
    assert not rcode, os.path.join(cijoe.output_path, cijoe.output_ident, "cmd.log")
