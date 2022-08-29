"""
    cijoe plugin for pytest
    =======================

    The plugin provides a cijoe-instance readily available as a test-fixture, setup per
    test with a nodeid-defined output-directory.

    pytest_addoption
    ----------------

      * --config
      * --output

    pytest_configure
    ----------------

    Initialized the cijoe instance using pytest-options '--config' and '--output'

    The cijoe-instance is stored in 'pytest.joe_instance', this might appear as bad
    form, however, pytest does not provide infrastructure for sharing state between
    fixtures, tests and utility functions, such as functions emitting
    parametrize-output.

    pytest_terminal_summary
    -----------------------

    Prints out a notice that CIJOE is beeing used along with the values of the
    '--config' and '--output' options.

    fixture: cijoe
    --------------

    Provides the cijoe instance ('pytest.joe_instance') with a per-test specific
    output-directory based on the test nodeid.
"""
from pathlib import Path

import pytest

from joe.core.command import Cijoe, default_output_path
from joe.core.resources import Collector, Config

pytest.cijoe_instance = None


def pytest_addoption(parser):

    collector = Collector()
    collector.collect()

    parser.addoption(
        "--config",
        action="store",
        type=Path,
        help="Path to CIJOE Environment Definition",
        default=collector.resources["configs"]["core.default"],
    )
    parser.addoption(
        "--output",
        action="store",
        type=Path,
        help="Path to auxilary output directory",
        default=default_output_path(),
    )


def pytest_configure(config):

    joe_config_path = config.getoption("--config")

    joe_config = Config.from_path(joe_config_path)
    if joe_config is None:
        raise Exception("Failed loading config")

    pytest.cijoe_instance = Cijoe(
        joe_config,
        config.getoption("--output"),
    )
    if pytest.cijoe_instance is None:
        raise Exception("Failed instantiating cijoe")


def pytest_terminal_summary(terminalreporter, exitstatus, config):
    """Provide a CIJOE section for pytest terminal report"""

    terminalreporter.ensure_newline()
    terminalreporter.section(
        "-={[ CIJOE pytest-plugin ]}=-", sep="-", blue=True, bold=True
    )
    terminalreporter.line("config: %r" % config.getoption("--config"))
    terminalreporter.line("output: %r" % config.getoption("--output"))


@pytest.fixture
def cijoe(request):
    """Constructs a CIJOE instance using pytest-options: 'config', and 'output'"""

    if pytest.cijoe_instance is None:
        raise Exception("Invalid configuration or instance")

    pytest.cijoe_instance.set_output_ident(request.node.nodeid)

    return pytest.cijoe_instance
