import joe.linux.null_blk as null_blk


def test_load_unload(cijoe):
    rcode = null_blk.insert(cijoe)
    assert not rcode, "Failed inserting kernel module"

    rcode = null_blk.remove(cijoe)
    assert not rcode, "Failed removing kernel module"
