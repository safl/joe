from pathlib import Path

import pytest

from joe.core.command import Cijoe, default_output_path
from joe.core.resources import Collector, Config

pytest.joe_instance = None


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
    print(joe_config_path)
    joe_config = Config.from_path(joe_config_path)
    if joe_config is None:
        raise Exception("Failed loading config")

    pytest.joe_instance = Cijoe(
        joe_config,
        config.getoption("--output"),
    )
    if pytest.joe_instance is None:
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
def cijoe(request, capsys):
    """Constructs a CIJOE instance using pytest-options: 'config', and 'output'"""

    if pytest.joe_instance is None:
        raise Exception("Invalid configuration or instance")

    pytest.joe_instance.set_output_ident(request.node.nodeid)

    return pytest.joe_instance
