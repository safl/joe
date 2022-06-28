import joe.linux.kmemleak as kmemleak


def test_clear(cijoe):

    rcode, state = kmemleak.clear(cijoe)
    assert not rcode, "Failed clearing kmemleak"


def test_scan(cijoe):

    rcode, state = kmemleak.scan(cijoe)
    assert not rcode, "Failed scanning kmemleak"


def test_cat(cijoe):

    rcode, state = kmemleak.cat(cijoe)
    assert not rcode, "Failed cat'ing kmemleak"
