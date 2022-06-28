import os

import pytest

be = {"dev-nsid": 0x1, "be": "linux", "admin": "nvme", "sync": "nvme"}


# This should invoked for each backend configuration
def test_cli_zoned_append(cijoe):

    slba = 0x0

    rcode, state = cijoe.run("zoned append {uri} --slba {slba} --nlb {nlb}")
    assert not rcode, os.path.join(cijoe.output_path, cijoe.output_ident, "cmd.log")

    rcode, state = cijoe.run("zoned append {uri} --slba {slba} --nlb {nlb}")
    assert not rcode, os.path.join(cijoe.output_path, cijoe.output_ident, "cmd.log")

    rcode, state = cijoe.run("zoned append {uri} --slba {slba} --nlb {nlb}")
    assert not rcode, os.path.join(cijoe.output_path, cijoe.output_ident, "cmd.log")

    rcode, state = cijoe.run("zoned append {uri} --slba {slba} --nlb {nlb}")
    assert not rcode, os.path.join(cijoe.output_path, cijoe.output_ident, "cmd.log")
