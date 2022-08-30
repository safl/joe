import cijoe.linux.null_blk as null_blk


def test_insert(cijoe):
    """Test the creation of null_block via module-load"""

    config = cijoe.config.options.get("null_blk", None)
    assert config, "Invalid environment configuration"

    nr_devices = int(config.get("nr_devices"))
    assert nr_devices, "!nr_devices, only module-load instances are supported"

    rcode, _ = null_blk.insert(cijoe)
    assert not rcode, "Failed inserting kernel module"

    rcode, _ = cijoe.run("lsblk")
    assert not rcode, "Failed listing block devices"

    for n in range(nr_devices):
        rcode, _ = cijoe.run(f"file /dev/nullb{n}")
        assert not rcode


def test_remove(cijoe):
    rcode, _ = null_blk.remove(cijoe)
    assert not rcode, "Failed removing kernel module"
