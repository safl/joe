from pathlib import Path

import pytest

from joe.core.command import Cijoe, default_output_path
from joe.core.resources import Collector, Config

JOE = None


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
    config.addinivalue_line(
        "markers", "rdonly(name): mark test as read-only, e.g. non-destructive"
    )


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

    global JOE

    if JOE:
        JOE.set_output_ident(request.node.nodeid)
        return JOE

    config = Config.from_path(request.config.getoption("--config"))
    if config is None:
        return None

    JOE = Cijoe(
        config,
        request.config.getoption("--output"),
    )
    JOE.set_output_ident(request.node.nodeid)

    return JOE
