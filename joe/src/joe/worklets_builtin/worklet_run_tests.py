import pytest


def worklet_entry(cijoe, args, step):
    """Invoke the test-runner"""

    pytest_args = ["--env", f"{args.env}", "--output", f"{args.output}"] + step.get(
        "with"
    ).get("args", "").split(" ")

    return pytest.main(pytest_args)
