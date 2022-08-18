# filetype=yaml
---
doc: |
  This workflow demonstrates how to use qemu via cijoe, specifically by:

  * Building qemu from source
  * Installing qemu to /opt/qemu
  * Provisioning a guest using a cloudinit image
  * Starting a guest
  * Stoppping a guest

  This is done via worklets, which in turn are utilizing helper-functions from core.qemu.wrapper

steps:
- name: build
  uses: qemu.build_x86

- name: install
  uses: qemu.install

- name: provision
  uses: qemu.guest_provision

- name: start
  uses: qemu.guest_start

- name: check
  run: |
    hostname

- name: kill
  uses: qemu.guest_kill

- name: report
  uses: core.reporter

- name: inspect
  uses: core.browser_open
