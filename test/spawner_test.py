from os import path

from parallelizer import spawner

# TODO: Re-enable this test when the following bug has been fixed in
# mozprocess:
#   Bug 935677 - Exit status reported by `wait` is incorrect
#   https://bugzilla.mozilla.org/show_bug.cgi?id=935677
def basic_xtest():
    """The generated performance report should correctly describe test
    duration, file names, and status code."""
    fixtures_dir = path.join(path.dirname(path.realpath(__file__)), 'fixtures')
    fixtures = ['pass.py', 'fail-23.py', 'fail-45.py']
    files = map(lambda fixture: [path.join(fixtures_dir, fixture)], fixtures)
    perf_report = spawner.spawn('python', files)

    assert(len(perf_report) == 3)

    for rep in perf_report:
        rep['duration'] = type(rep['duration']) == float and rep['duration'] > 0

    assert({ 'file_names': files[0], 'duration': True, 'status': 0 } in perf_report)
    assert({ 'file_names': files[1], 'duration': True, 'status': 23 } in perf_report)
    assert({ 'file_names': files[2], 'duration': True, 'status': 45 } in perf_report)
