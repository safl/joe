import os

import yaml

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


def dict_from_yaml(yaml_path):
    """Load the yaml-file, return {} on empty document."""

    with open(yaml_path, "r") as yaml_file:
        return yaml.safe_load(yaml_file) or {}
