import joe.fio.wrapper as fio
import joe.linux.null_blk as null_blk


def test_run(cijoe):

    rcode, _ = null_blk.insert(cijoe)
    assert not rcode

    rcode, _ = fio.run(
        cijoe,
        [
            "--filename",
            "/dev/nullb0",
            "--bs",
            "4k",
            "--rw",
            "randread",
            "--size",
            "1G",
            "--name",
            "foo42",
        ],
    )
    assert not rcode
