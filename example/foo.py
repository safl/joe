#!/usr/bin/env python
from pathlib import Path

import yaml


def main():
    """Entry function for importing joe cli options"""

    path = Path("example.workflow").resolve()
    with path.open("r") as yfile:
        yml = yaml.load(yfile, Loader=yaml.SafeLoader)

    if "steps" not in yml:
        return 0

    print(" ".join([step["name"] for step in yml["steps"] if "name" in step]))


if __name__ == "__main__":
    main()
