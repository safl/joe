import os

import pytest


def worklet_entry(cijoe, args, step):
    """Invoke the test-runner"""

    print("# OUTPUT from the test_runner-worklet")

    pytest_args = ["--output", str(args.output / cijoe.output_ident)]

    config_path = cijoe.get_config_fpath()
    if config_path:
        pytest_args.append("--env")
        pytest_args.append(str(config_path))

    pytest_args += step.get("with").get("args", "").split(" ")

    return pytest.main(pytest_args)
