"""
    fio-wrapper
    ===========

    config
    ------

    fio.bin

    fio.engines

    retargtable: true
    -----------------
"""
import errno
import logging as log


def fio(cijoe, args="", env={}):
    """Invoke 'fio'"""

    return cijoe.run(f"{cijoe.config.options['fio']['bin']} {args}", env=env)


def fio_script_engine(
    cijoe,
    script,
    section,
    engine_name,
    device,
    be_opts,
    output_path,
    extra_args,
    env={},
):
    """
    Invoke fio with special setup of external IO-engine parameters
    """

    args = []

    # Script and section
    args += [
        str(script),
        f"--section={section}"
    ]

    # Retrieve engine information
    engines = cijoe.config.options.get("fio", {}).get("engines", None)
    if engines is None:
        log.error("Configuration has no 'engines'")
        return errno.EINVAL, None
    engine = engines.get(engine_name, None)
    if engine is None:
        log.error(f"Configuration has no 'engine' with label({engine_name})")
        return errno.EINVAL, None

    # setup general '--ioengine' options
    if engine["type"] == "builtin":
        args.append(f"--ioengine={engine_name}")
    elif engine["type"] == "external_dynamic":
        args.append(f"--engine=external:{ engine['path'] }")
        args.append(f"--filename={device['uri']}")
    elif engine["type"] == "external_preload":
        args = [f"LD_PRELOAD={ engine['path'] }"] + args
        args.append(f"--filename={device['uri']}")
    else:
        log.error(f"Configuration has invalid engine.type({ engine['type'] })")
        return errno.EINVAL, None

    # setup 'xnvme' specific options
    if engine_name == "xnvme":
        args.append(f"--xnvme_async={ be_opts['async'] }")
        args.append(f"--xnvme_sync={ be_opts['sync'] }")
        args.append(f"--xnvme_admin={ be_opts['admin'] }")
        args.append(f"--xnvme_dev_nsid={ device['nsid'] }")
        args.append(f"--filename={device['uri']}")
    elif engine_name == "spdk":
        args.append(
            f"--filename=\"trtype=PCIe traddr={device['uri']} ns={device['nsid']}\""
        )
    elif engine_name == "spdk_bdev":
        # generate spdk-conf
        spdk_conf = []
        spdk_conf.append("[Nvme]")
        spdk_conf.append("  TransportID \"trtype:PCIe traddr:{device['uri']\" Nvme0")

        args.append("--spdk_conf=/tmp/spdk.bdev.conf")
        args.append("--filename=Nvme0n1")
        # TODO: add subnqn here

    args += [
        "--output-format=normal,json",
        f"--output=/tmp/fio-output.txt"
    ]

    # Add extra arguments
    args += extra_args

    rcode, state = fio(cijoe, " ".join(args), env=env)

    cijoe.get("/tmp/fio-output.txt", ".")

    return rcode, state
