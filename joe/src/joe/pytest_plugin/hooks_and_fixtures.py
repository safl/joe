import pytest

from joe.core.command import Cijoe, default_output_path

JOE = None


def pytest_addoption(parser):
    parser.addoption(
        "--config",
        action="store",
        help="Path to CIJOE Environment Definition",
        default=None,
    )
    parser.addoption(
        "--output",
        action="store",
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

    JOE = Cijoe(
        request.config.getoption("--config"),
        request.config.getoption("--output"),
    )
    JOE.set_output_ident(request.node.nodeid)

    return JOE
