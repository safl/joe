import joe.linux.null_blk as null_blk
import joe.fio.wrapper as fio

def test_run(cijoe):

    rcode, state = null_blk.insert(cijoe)
    assert not rcode

    rcode, state = fio.run(cijoe, ["--filename", "/dev/nullb0"], cwd, evars)
    assert not rcode
