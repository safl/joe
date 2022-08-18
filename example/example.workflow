# filetype=yaml
---
doc: |
  This is an example of utilizing some of the Linux worklets and helpers

steps:
- name: sysinfo
  uses: linux.sysinfo

- name: null_blk_insert
  uses: linux.null_blk

- name: list
  run: lsblk

- name: null_blk_remove
  uses: linux.null_blk
  with:
    do: remove

- name: report
  uses: core.reporter

- name: report_open
  uses: core.browser_open
