from os import path

import mozprocess

from get_fixture import get_fixture

here = path.dirname(path.realpath(__file__))
runner_location = path.join(here, 'fake_runner.py')
parallelizer_location = path.join(here, '..', '..', 'parallelizer', 'parallelizer.py')

def run_fixtures(file_names):
    """Use the Parallelizer to run a list of test fixtures using the "fake"
    runner. Return the process's exit status."""
    file_names = map(get_fixture, file_names)
    args = [parallelizer_location, '-c', 'python'] + file_names
    process = mozprocess.ProcessHandlerMixin(
        cmd='python',
        args=args
    )
    process.run()
    return process.wait()

def normal_test():
    "When none of the test files fail, the process exits with status code 0"
    assert run_fixtures(['pass.py', 'pass.py']) == 0

def failure_test():
    "When one test file fails, the process exits with status code 1"
    status = run_fixtures(['pass.py', 'fail.py'])
    print "Received status: ", status
    assert status > 0
