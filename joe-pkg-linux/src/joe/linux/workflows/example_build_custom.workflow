# filetype=yaml
---
doc: |
  This is an example of utilizing some of the Linux worklets and helpers

steps:
- name: sysinfo
  uses: linux.sysinfo


- name: report
  uses: core.reporter
  with:
    report_open: true
