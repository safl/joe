import os

import pytest


def worklet_entry(cijoe, args, step):
    """Invoke the test-runner"""

    print("#")
    print("# OUTPUT from the test_runner-worklet")
    print("#")

    env_fpath = cijoe.get_config_fpath()
    output = os.path.join(args.output, cijoe.output_ident)

    pytest_args = ["--output", f"{output}"]

    if env_fpath:
        pytest_args.append("--env")
        pytest_args.append(f"{env_fpath}")

    pytest_args += step.get("with").get("args", "").split(" ")

    return pytest.main(pytest_args)
