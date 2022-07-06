import os


def worklet_entry(cijoe, args, step):
    """Produce a report of a workflow run"""

    for root, dirnames, filenames in os.walk(cijoe.output_path, topdown=True):
        for filename in filenames:
            print(os.path.join(root, filename))

    print("report")
