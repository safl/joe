import os


# This should invoked for each backend configuration
def test_cli_zoned_append(cijoe):

    slba = 0x0
    nlb = 0
    uri = "/dev/nvme0n1"

    rcode, state = cijoe.run(f"zoned append {uri} --slba {slba} --nlb {nlb}")
    assert not rcode, os.path.join(cijoe.output_path, cijoe.output_ident, "cmd.log")

    rcode, state = cijoe.run(f"zoned append {uri} --slba {slba} --nlb {nlb}")
    assert not rcode, os.path.join(cijoe.output_path, cijoe.output_ident, "cmd.log")

    rcode, state = cijoe.run(f"zoned append {uri} --slba {slba} --nlb {nlb}")
    assert not rcode, os.path.join(cijoe.output_path, cijoe.output_ident, "cmd.log")

    rcode, state = cijoe.run(f"zoned append {uri} --slba {slba} --nlb {nlb}")
    assert not rcode, os.path.join(cijoe.output_path, cijoe.output_ident, "cmd.log")
