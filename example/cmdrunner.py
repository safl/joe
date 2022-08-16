
def worklet_entry(args, collector, cijoe, step):
    """Run commands listedin step['run']"""

    rcode = 0

    for cmd in step["run"]:
        rcode, state = cijoe.run(cmd)
        if rcode:
            break

    return rcode
