import joe.linux.null_blk as null_blk


def test_insert(cijoe):
    rcode, _ = null_blk.insert(cijoe)
    assert not rcode, "Failed inserting kernel module"


def test_remove(cijoe):
    rcode, _ = null_blk.remove(cijoe)
    assert not rcode, "Failed removing kernel module"
