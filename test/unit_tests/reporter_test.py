import operator

from get_fixture import get_fixture

import parallelizer.reporter as reporter
Reporter = reporter.Reporter

class MockStrictRedis(reporter.redis.StrictRedis):
    def __init__(self, **kwargs):
        self._calls = dict(mget=[], setex=[])
    def mget(self, *args):
        self._calls['mget'].append(args)
        return map(str, range(1, len(args) + 1))
    def setex(self, *args):
        self._calls['setex'].append(args)
    def pipeline(self):
        return self
    def execute(self):
        return self._calls

reporter.redis.StrictRedis = MockStrictRedis

fixtures = map(file, map(get_fixture, ['fail.py', 'pass.py']))

def get_report_normal_test():
    """The generated performance report should have two fields: a file name and
    a weight."""
    r = Reporter('localhost', 0)

    report = r.get_report(fixtures)

    assert len(report) == 2
    assert dict(file_name=fixtures[0].name, weight=1) in report
    assert dict(file_name=fixtures[1].name, weight=2) in report

def get_report_one_new_test():
    """Unrecognized test files should be given a nonzero weight in the
    generated performance report."""
    MockStrictRedis.mget = lambda *args: [None] + map(str, range(1, len(args)))
    r = Reporter('localhost', 0)

    report = r.get_report(fixtures)

    assert len(report) == 2
    assert type(report[0]['weight']) == float
    assert type(report[1]['weight']) == float
    assert report[0]['weight'] > 0
    assert report[1]['weight'] > 0

def get_report_all_new_test():
    """The performance report generated for all unrecognized test files should
    specify some constant non-zero weight."""
    MockStrictRedis.mget = lambda *args: [None] * len(args)
    r = Reporter('localhost', 0)

    report = r.get_report(fixtures)

    assert len(report) == 2
    assert type(report[0]['weight']) == float
    assert report[0]['weight'] > 0
    assert report[0]['weight'] == report[1]['weight']

def submit_normal_report():
    """The perforance report is submitted as expected."""
    r = Reporter('localhost', 0)
    report = [
      dict(file_name=fixtures[0].name, weight=20),
      dict(file_name=fixtures[1].name, weight=30)
    ]

    setex_calls = r.submit(report)['setex']
    weights = map(operator.itemgetter('weight'), setex_calls)

    assert len(setex_calls) == 2
    assert 20 in weights
    assert 30 in weights
