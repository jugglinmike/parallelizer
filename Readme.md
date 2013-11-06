# Parallelizer

A tool for efficiently scheduling test execution. See [Bug 931087 - [meta]
Amazing parallel test runner (and metrics,
etc..)](https://bugzilla.mozilla.org/show_bug.cgi?id=931087).

## Installation

Install the tool by running:

    $ python setup.py develop

## Tests

After installations, the project's tests can be run via:

    $ nosetests

## Resources

- [mach](https://developer.mozilla.org/en-US/docs/Developer_Guide/mach) - a
  command-line interface to help developers perform common tasks. The purpose
  of mach is to help make the developer experience better by making common
  tasks easier to discover and perform.
- [mozbase](https://github.com/mozilla/mozbase) - Base utilties for mozilla
  test harnesses (see specifically
  [mozprocess](https://github.com/mozilla/mozbase/tree/master/mozprocess))