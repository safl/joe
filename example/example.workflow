# filetype=yaml
---
doc: |
  This workflow demonstrates how to use qemu via cijoe, specifically by:

  * building qemu
  * installing qemu
  * provisioning a guest
  * starting a guest
  * stoppping a guest

  This is done via worklets, which in turn are utilizing a qemu-wrapper

steps:
- name: info
  run: |
    cat /proc/cpuinfo
    hostname

- name: test
  uses: core.testrunner
  with:
    args: ""

- name: report
  uses: reporter

- name: inspect
  uses: core.browser_open
