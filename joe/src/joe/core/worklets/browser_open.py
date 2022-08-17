"""
    Open generated report, if it exists.
"""
import webbrowser
from pathlib import Path

from joe.core.resources import collector


def worklet_entry(args, cijoe, step):
    """Produce a HTML report of the 'workflow.state' file in 'args.output'"""

    collector.collect()

    url = Path(args.output).resolve() / "report.html"
    if "with" in step and "args" in step["with"] and "url" in step["with"]["args"]:
        url = step["with"]["args"]["url"]

    if isinstance(url, Path) and not url.exists():
        print(f"url: '{url}', does not exist, not opening.")

    webbrowser.open(str(url))

    return 0
