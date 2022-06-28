import argparse


def analyse():
    print("analyse()")


def extract():
    print("extract()")


def report():
    print("report()")


def pytest():
    print("invoking pytest")


CLI = {
    "pytest": {"func": pytest, "parser": None, "help": "bar"},
    "extract": {"func": extract, "parser": None, "help": "bar"},
    "analyse": {"func": analyse, "parser": None, "help": "foo"},
    "report": {"func": report, "parser": None, "help": "baz"},
}


def parse_args():
    """Parse command-line interface."""

    parser = argparse.ArgumentParser(prog="joe")
    parser.add_argument("--version", action="store_true", help="Show version")

    subparsers = parser.add_subparsers(required=True, help="sub-command help")

    for ident, cli in CLI.items():
        cli["parser"] = subparsers.add_parser(ident, help=cli["help"])
        cli["parser"].add_argument("--output", help="Path to test-results")

    return parser.parse_args()


def main():
    """Main entry point for the CLI"""

    print("hello from cli")

    args = parse_args()
    print(args)
