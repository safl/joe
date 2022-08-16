#!/usr/bin/env python
import yaml
import pprint
import jinja2
import os
from pathlib import Path



def main():
    with open('default.config') as fd:
        yml = yaml.safe_load(fd)

    traverse(yml)

    pprint.pprint(yml)

if __name__ == "__main__":
    main()
