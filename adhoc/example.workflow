---
docstring: |
  This is a workflow file, it serves as an example on how to run commands and use worklets, the
  structure intentionally mimics that of GitHUB actions, however, the keys you see here are all
  there is.

  Running commands, as you can see below, looks just like running commands in a GitHUB Workflow

  * Add the 'run' key with a value of multi-line string

  Using worklets, it is similar to that of a GitHUB action

  * Add the 'uses' key with the name of the worklet
  * Add the 'with' key providing arguments to the worklet

  The commands and the worklets are passed an instance of cijoe which they can use to call
  run()/get()/put(), with an output-directory matching the current step. This is it, end of story.

steps:
- name: Invoke commands via cijoe.run()
  run: |
    cat /proc/cpuinfo
    hostname

- name: Build it!
  uses: build_jazz

- name: Build it!
  uses: deploy_jazz

- name: Invoke the test_runner worklet
  uses: core.run_tests
  with:
    args: "--pyargs joe.core.selftest"

- name: Invoke the report generator worklet
  uses: core.report
