from os import path

from parallelizer import spawner
from parallelizer.logger import Logger

# TODO: Re-enable this test when the following bug has been fixed in
# mozprocess:
#   Bug 935677 - Exit status reported by `wait` is incorrect
#   https://bugzilla.mozilla.org/show_bug.cgi?id=935677
def basic_xtest():
    """The generated performance report should correctly describe test
    execution duration, file name, and status code."""
    fixtures_dir = path.join(path.dirname(path.realpath(__file__)), 'fixtures')
    fixtures = ['pass.py', 'fail-23.py', 'fail-45.py']
    files = map(lambda fixture: [path.join(fixtures_dir, fixture)], fixtures)
    perf_report = spawner.spawn('python', files, Logger())

    assert(len(perf_report) == 3)

    def assert_shape(report):
        assert(len(report) == 1)
        assert(type(report[0]['duration']) == float)
        assert(report[0]['duration'] > 0)

    # Remove unecessary structure and non-deterministic data
    def collapse(report):
        del report[0]['duration']
        return report[0]

    (assert_shape(report) for report in perf_report)

    collapsed = map(collapse, perf_report)

    assert({ 'file_name': files[0][0], 'status': 0 } in collapsed)
    assert({ 'file_name': files[1][0], 'status': 23 } in collapsed)
    assert({ 'file_name': files[2][0], 'status': 45 } in collapsed)
