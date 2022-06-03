def test_hello():

    assert True


def test_default(cijoe):

    rcode, state = cijoe.cmd("ls -lh")

    assert rcode == 0


def test_default_again(cijoe):

    rcode, state = cijoe.cmd("ls")

    assert rcode == 0
