import os


def worklet_entry(cijoe, args, step):
    """Produce a report of a workflow run"""

    print("#")
    print("# HELLO from the report-worklet")
    print("#")

    for root, dirnames, filenames in os.walk(args.output, topdown=True):
        for filename in filenames:
            print(os.path.join(root, filename))

    print("# HEYOO")
