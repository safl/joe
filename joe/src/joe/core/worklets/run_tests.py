import pytest


def worklet_entry(args, collector, cijoe, step):
    """Invoke the test-runner"""

    pytest_args = ["--output", str(args.output / cijoe.output_ident)]
    pytest_args += [
        "--report-log",
        str(args.output / cijoe.output_ident / "pytest.log"),
    ]

    config_path = cijoe.get_config_fpath()
    if config_path:
        pytest_args.append("--config")
        pytest_args.append(str(config_path))

    pytest_args += step.get("with").get("args", "").split(" ")

    return pytest.main(pytest_args)
