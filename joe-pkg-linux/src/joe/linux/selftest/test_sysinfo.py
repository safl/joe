import joe.linux.sysinfo as sysinfo


def test_sysinfo_collect(cijoe):

    rcode = sysinfo.collect(cijoe)

    assert not rcode, "Failed collecting Linux system information"
