import pytest

from joe.core.command import Cijoe, default_output_path, env_from_file

JOE = None


def pytest_addoption(parser):
    parser.addoption(
        "--env",
        action="store",
        help="Path to CIJOE Environment Definition",
        default="default.yml",
    )
    parser.addoption(
        "--output",
        action="store",
        help="Path to auxilary output directory",
        default=default_output_path(),
    )


def pytest_terminal_summary(terminalreporter, exitstatus, config):
    """Provide a CIJOE section for pytest terminal report"""

    terminalreporter.ensure_newline()
    terminalreporter.section("CIJOE", sep="-", blue=True, bold=True)
    terminalreporter.line("env: %r" % config.getoption("--env"))
    terminalreporter.line("output: %r" % config.getoption("--output"))


@pytest.fixture
def cijoe(request, capsys):
    """Constructs a CIJOE instance using pytest-options: 'env', and 'output'"""

    global JOE

    if JOE:
        JOE.set_output_ident(request.node.nodeid)
        return JOE

    JOE = Cijoe(
        env_from_file(request.config.getoption("--env")),
        request.config.getoption("--output"),
    )
    JOE.set_output_ident(request.node.nodeid)

    return JOE


@pytest.fixture
def nvme(cijoe, capsys):

    nvme = cijoe.get_env(subject="nvme")
    if not nvme:
        return None

    for device in nvme.get("devices", []):
        return device

class Xnvme(object):

    def __init__(self, cijoe):
        self.cijoe = cijoe

    def reset(self):

        rcode, state = self.cijoe.transport

@pytest.fixture
def xnvme(cijoe, capsys):

    nvme = cijoe.get_env(subject="nvme")
    if not nvme:
        return None

    for device in nvme.get("devices", []):
        return device
