def test_hello():

    assert True


def test_default(cijoe):

    rcode, state = cijoe.run("ls -lh")

    assert rcode == 0


def test_default_again(cijoe):

    rcode, state = cijoe.run("ls")

    assert rcode == 0
