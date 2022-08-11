# filetype=yaml
---
doc: |
  This workflow builds and installs qemu with system-x86, provisions a guest and boots it
  it.

steps:
- name: info
  run: |
    cat /proc/cpuinfo
    hostname

- name: build
  uses: qemu.build_x86

- name: install
  uses: qemu.install

- name: report
  uses: core.reporter

- name: inspect
  uses: core.browser_open
