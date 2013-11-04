How it works in jlal's head

- node process which spawns other processes and aggregates their output in real time (to a magic parallel runner format)


# Parallel Runner API description

Name
    paralleltest - spawn and benchmark multiple test-running processes

Synopsis
    paralleltest <options> <test files | manifest>

Options
    --reporter, -r name
        The reporter to use. Valid options:
        - json-stream
        - tbpl
        - tap

    --exec, -e cmd
        The command to execute. This process should accept a filename as an
        argument, and it should output one of the following test reporting
        protocols to standard out:
        - TAP
        - TBPL

    --timeout, -t s
        Number of seconds to wait before considering a silent process "failed" and
        killing it

Examples
    paralleltest --reporter json-stream \
        --exec "test-agent -x --reporter tap" -- file_a.js file_b.js file_c.js
    parelleltest --exec "./bin/gaia-ui-test" --reporter tap tests/python/gaia-ui-tests/gaiatest/tests/tbpl-manifest.ini

# Implementation details

- **Should be implemented with Python.**
- Utilize mach: https://developer.mozilla.org/en-US/docs/Developer_Guide/mach
- use mozprocess for process management ( https://github.com/mozilla/mozbase/tree/master/mozprocess )
- jgriffin is available for feedback

## Features

### Manifest files

A file that lists input files, along with conditions that describe when they should be run. 
Should be a `.ini` file
Example from gaia-ui-tests: https://github.com/mozilla-b2g/gaia/blob/master/tests/python/gaia-ui-tests/gaiatest/tests/functional/browser/manifest.ini

### Real-time reporting

### Performance reporting
- Collect metrics:
    - Time-per-test
    - Memory (for scaling across machines)
    - CPU consumption (for scaling across machines)
- Recording
    - To a file within a local .directory
    - To an in-memory database, possibly Redis

# Scheduling

## Feature schedule

1. TAP output/input
    a. possibly mozlog structured logging format as well
2. Adaptive scheduling
    a. Performance reporting
    b. Adaptive scheduling
3. TPBL output/input
4. Real-time reporting
5. Manifest support

## Deployment schedule

1. Gaia-UI (Python) tests
2. Marionette (JavaScript) tests
3. Test-agent unit tests

# Background

## Test Environments

- TravisCI: 2 cores
- AWS: 1.5 or 2 cores
- Developers: 2+ cores

## Treeherder

The backend of treeherder, a replacement for TBPL.
https://github.com/mozilla/treeherder-service

