import pytest
import os


def worklet_entry(cijoe, args, step):
    """Invoke the test-runner"""

    output = os.path.join(args.output, cijoe.output_ident)

    pytest_args = ["--env", f"{args.env}", "--output", f"{output}"] + step.get(
        "with"
    ).get("args", "").split(" ")

    return pytest.main(pytest_args)
