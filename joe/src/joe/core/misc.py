import errno
import os
from pathlib import Path

import requests

ENCODING = "UTF-8"
HEADER_MIN = 60


def line(title=None, marker=None):
    """Print a header"""

    if not title:
        title = ""
    if not marker:
        marker = "#"

    try:
        width, _ = os.get_terminal_size()
    except Exception:
        width = HEADER_MIN

    if width < HEADER_MIN:
        width = HEADER_MIN

    print(
        (marker if not title else " ").join(
            [marker * 2, title, marker.ljust(width - 4 - len(title), marker)]
        )
    )


def h1(title=""):
    line(title, "#")


def h2(title=""):
    line(title, "=")


def h3(title=""):
    line(title, "-")


def h4(title=""):
    line(title, " ")


def download(url: str, path: Path):
    """Downloads a file over http(s), returns (err, path)."""

    path = Path(path).resolve()
    if path.is_dir():
        path = path / url.split("/")[-1]
    if not (path.parent.is_dir() and path.parent.exists()):
        return errno.EINVAL, path

    with requests.get(url, stream=True) as request:
        request.raise_for_status()
        with path.open("wb") as local:
            for chunk in request.iter_content(chunk_size=8192):
                local.write(chunk)

    return 0, path
