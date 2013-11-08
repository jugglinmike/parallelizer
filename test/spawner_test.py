from os import path
import operator

from parallelizer import spawner
from parallelizer.logger import Logger

def basic_test():
    """The generated performance report should correctly describe test
    execution duration, and file name of only those files which exited with
    successful error codes."""
    fixtures_dir = path.join(path.dirname(path.realpath(__file__)), 'fixtures')
    fixtures = ['pass.py', 'fail.py', 'fail.py', 'pass.py']
    files = map(lambda fixture: [path.join(fixtures_dir, fixture)], fixtures)
    perf_report = spawner.spawn('python', files, Logger())

    assert(len(perf_report) == 2)

    def assert_shape(report):
        assert(type(report['duration']) == float)
        assert(report['duration'] > 0)

    (assert_shape(report) for report in perf_report)

    report_files = map(operator.itemgetter('file_name'), perf_report)

    assert(files[0][0] in report_files)
    assert(files[3][0] in report_files)
