#!/usr/bin/env python3
from joe.core.collector import (
    iter_config_fpaths,
    iter_template_fpaths,
    iter_testfile_fpaths,
)

print(list(iter_config_fpaths()))
print(list(iter_template_fpaths()))
print(list(iter_testfile_fpaths()))
