import errno


def worklet_entry(args, collector, cijoe, step):
    """Run commands one at a time via cijoe.run()"""

    rcode = 0
    if "with" not in step and "commands" not in step["with"]:
        return errno.EINVAL

    for cmd in step["with"]["commands"]:
        rcode, state = cijoe.run(cmd)
        if rcode:
            break

    return rcode
