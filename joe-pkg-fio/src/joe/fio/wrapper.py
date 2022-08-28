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
import logging as log
import errno


def fio(cijoe, args=""):
    """Invoke 'fio'"""

    return cijoe.run(f"{cijoe.config.options['fio']['bin']} {args}")


def fio_script_engine(
    cijoe, script, script_section, engine_label, device, be_opts, filename, output_path
):
    """
    Invoke 'fio' script with setup of io-engine
    """

    args = []

    # Retrieve engine information
    engines = cijoe.config.options.get("engines", None)
    if engines is None:
        log.err("Configuration has no 'engines'")
        return errno.EINVAL, None
    engine = cijoe.config.options.get(engine_label, None)
    if engine is None:
        log.err(f"Configuration has no 'engine' with label({engine_label})")
        return errno.EINVAL, None

    # setup '--ioengine' options
    if engine["type"] == "builitin":
        args.append(f"--ioengine={engine_label}")
    elif engine["type"] == "external_dynamic":
        args.append(f"--engine=external:{ engine['path'] }")
        args.append(f"--filename={filename}")
    elif engine["type"] == "external_preload":
        args = [f"LD_PRELOAD={ engine['path'] }"] + args
        args.append(f"--filename={filename}")
    else:
        log.err(f"Configuration has invalid engine.type({ engine['type'] })")
        return errno.EINVAL, None

    # setup 'xnvme' specific options
    if engine_label == "xnvme":
        args.append(f"--xnvme_async={ be_opts['async'] }")
        args.append(f"--xnvme_sync={ be_opts['sync'] }")
        args.append(f"--xnvme_admin={ be_opts['admin'] }")
        args.append(f"--xnvme_dev_nsid={ device['nsid'] }")
        # TODO: add subnqn here

    if device:
        args.append(f"--filename={ device['uri'] }")

    rcode, _ = fio(cijoe, " ".join(args))
