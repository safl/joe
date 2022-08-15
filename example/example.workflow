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
    hostname
    lsblk
    lscpu
    lsipc
    lslocks
    lslogins
    lsmem
    lsmod
    lsns
    lspci
    lsusb

- name: test
  uses: core.testrunner
  with:
    args: "--pyargs joe.core.selftest"

- name: report
  uses: reporter

- name: inspect
  uses: core.browser_open
