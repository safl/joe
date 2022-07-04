import argparse


def analyse(args):
    print("analyse()")


def extract(args):
    print("extract()")


def report(args):
    print("report()")


def run(args):
    print("invoking pytest")


def parse_args():
    """Parse command-line interface."""

    parser = argparse.ArgumentParser(prog="joe")
    parser.add_argument("--version", action="store_true", help="Show version")

    subparsers = parser.add_subparsers(dest="func", help="sub-command help")

    parser_run = subparsers.add_parser("run", help="Invoke the test-runner")
    parser_run.set_defaults(func=run)
    parser_run.add_argument("--env", help="Path to the environment definition")
    parser_run.add_argument("--workflow", help="Path to a workflow.yaml")
    parser_run.add_argument("--output", help="Path to test-results")

    parser_analyse = subparsers.add_parser("analyse", help="Invoke the analyser")
    parser_analyse.set_defaults(func=analyse)
    parser_analyse.add_argument("--output", help="Path to test-results")

    parser_extract = subparsers.add_parser("extract", help="Invoke the test-runner")
    parser_extract.set_defaults(func=extract)
    parser_extract.add_argument("--output", help="Path to test-results")

    parser_report = subparsers.add_parser("report", help="Invoke the test-runner")
    parser_report.set_defaults(func=report)
    parser_report.add_argument("--output", help="Path to test-results")

    return parser.parse_args()


def main():
    """Main entry point for the CLI"""

    args = parse_args()
    if args.func:
        args.func(args)
