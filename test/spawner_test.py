import operator

from utils import get_fixture

from parallelizer import spawner
from parallelizer.logger import Logger

def basic_test():
    """The generated performance report should correctly describe test file
    name and "weight" of only those files which exited with successful error
    codes."""
    fixture_names = ['pass.py', 'fail.py', 'fail.py', 'pass.py']
    files = map(lambda name: [get_fixture(name)], fixture_names)
    perf_report = spawner.execute('python', files, Logger())

    assert(len(perf_report) == 2)

    for report in perf_report:
        assert(type(report['weight']) == float)
        assert(report['weight'] > 0)

    report_files = map(operator.itemgetter('file_name'), perf_report)

    assert(files[0][0] in report_files)
    assert(files[3][0] in report_files)
