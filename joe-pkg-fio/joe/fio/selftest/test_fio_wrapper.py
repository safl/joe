import joe.fio.wrapper as fio
import joe.linux.null_blk as null_blk


def test_run(cijoe):

    rcode, state = null_blk.insert(cijoe)
    assert not rcode

    rcode, state = fio.run(cijoe, ["--filename", "/dev/nullb0"], cwd, evars)
    assert not rcode
