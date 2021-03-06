# Parallelizer

A tool for efficiently scheduling test execution. See [Bug 931087 - [meta]
Amazing parallel test runner (and metrics,
etc..)](https://bugzilla.mozilla.org/show_bug.cgi?id=931087).

## Installation

Requirements:

- Python 2.7 (download from [python.org](http://python.org/download/))
- Redis 2.2.12 or greater running either locally or at a network-accessible
  location (download from [redis.io](http://redis.io/download))

Install the tool by running:

    $ python setup.py develop

## Usage

The project installs a single executable in properly-configured environments:
`parallelizer`. This project is under heavy development, so in leui of formal
usage documentation, please invoke the executable with the `--help` flag:

    $ parallelizer --help

## Terminology

The following terms have a specific meaning in this project, and understanding
them will help in reading the source:

- **performance report** - a list of test file-*weight* pairs
- **weight** - a rough metric for test file resource needs, crudely normalized
  against system capabilities
- **schedule** - a list of *jobs*
- **job** - a list of test files

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
