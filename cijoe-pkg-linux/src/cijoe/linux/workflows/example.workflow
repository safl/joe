# filetype=yaml
---
doc: |
  This is an example of utilizing some of the Linux worklets and helpers

steps:
- name: sysinfo
  uses: linux.sysinfo

- name: build
  uses: linux.build_deb
