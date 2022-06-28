from joe.linux.wrapper import insert, remove


def test_load_unload(cijoe):
    rcode = insert()
    assert not rcode, "Failed insert kernel module"

    rcode = remove()
    assert not rcode, "Failed removing kernel module"
