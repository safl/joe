"""
    Open generated report, if it exists.
"""
from pathlib import Path
import webbrowser

def worklet_entry(args, collector, cijoe, step):
    """Produce a HTML report of the 'workflow.state' file in 'args.output'"""

    report_path = Path(args.output).resolve() / "report.html"

    if not report_path.exists():
        print(f"report_path: '{report_path}', does not exist, not opening.")

    return webbrowser.open(str(report_path))
