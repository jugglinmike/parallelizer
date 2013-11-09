import operator

def make(perf_report, parallelism):
    """Create an object representing the optimal schedule of test runs. Uses
    a simple greedy algorithm."""

    # Create a 'full' job schedule for each slot
    full_schedule = [ { 'weight': 0, 'files': [] }
        for _ in range(parallelism) ]

    perf_report.sort(key=operator.itemgetter('weight'), reverse=True)

    for file_report in perf_report:
        proc = min(full_schedule, key=operator.itemgetter('weight'))

        proc['weight'] += file_report['weight']
        proc['files'].append(file_report)

    return _simplify_schedule(full_schedule)

def _simplify_schedule(full_schedule):
    """Reduce a 'full' schedule (which contains 'full' job reports) to a
    two-dimensional list of file names."""
    schedule = map(_simplify_job, full_schedule)
    # Remove empty job schedules
    schedule = filter(lambda files: len(files), schedule)
    return schedule

def _simplify_job(job):
    """Reduce a 'full' job report (which specifies a total duration and
    per-file timing data) to a simple list of file names."""
    return map(operator.itemgetter('file_name'), job['files'])
