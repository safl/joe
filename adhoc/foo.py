#!/usr/bin/env python3
from joe.core.collector import iter_template_fpaths
from joe.core.collector import iter_config_fpaths
from joe.core.collector import iter_testfile_fpaths

print(list(iter_config_fpaths()))
print(list(iter_template_fpaths()))
print(list(iter_testfile_fpaths()))
