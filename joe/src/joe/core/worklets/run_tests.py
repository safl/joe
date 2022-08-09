"""
  Invokes 'pytest' for cijoe testcases

  It is intended for a specific use of pytest with the plugins listed below, it is as
  such not a completely open-ended pytest-invocation as the cijoe-testcases must utilize
  'cijoe.run' etc. to encapsulate command-execution, capture command output, and
  collector artifacts.

  Requires the following pytest plugins for correct behaviour:

  * cijoe, fixtures providing 'cijoe' object and "--config" and "--output"
    pytest-arguments to instantiate cijoe.
  * report-log, dump testnode-status as JSON, this is consumed by 'core.report' to
    produce an overview of testcases and link them with the cijoe-captured output and
    auxilary files
"""
import pytest


def worklet_entry(args, collector, cijoe, step):
    """Invoke test-runner"""

    pytest_args = ["--output", str(args.output / cijoe.output_ident)]
    pytest_args += [
        "--report-log",
        str(args.output / cijoe.output_ident / "pytest.log"),
    ]

    if args.config:
        pytest_args.append("--config")
        pytest_args.append(str(args.config))

    pytest_args += step.get("with").get("args", "").split(" ")

    return pytest.main(pytest_args)
