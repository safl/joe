import pytest


def worklet_entry(cijoe, args, step):
    """Invoke the test-runner"""

    return pytest.main(
        " ".join(["--env", f"{args.env}", "--output", f"{args.output}"]) + step["args"]
    )
