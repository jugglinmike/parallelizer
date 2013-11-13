import time
import os
from concurrent import futures

import mozprocess
from utils.curry import curry
from utils.cpu_count import cpu_count

def parallelism():
    return cpu_count()

def execute(cmd, schedule, logger):
    """Asynchronously execute the tests described by the specified command and
    schedule. Return a performance report containing a 'score' for each file
    that terminated normally."""

    durations = run_jobs(cmd, schedule, logger)
    perf_report = make_report(durations, logger)
    return perf_report

def make_report(durations, logger):
    """Given a duration report, create a performance report by normalizing raw
    timing data according to the local system's resources."""
    benchmarks = ['cpu', 'memory', 'disk']
    benchmark_dir = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        'benchmarks'
    )
    benchmarks = map(lambda x: [os.path.join(benchmark_dir, x) + '.py'], benchmarks)

    benchmark_report = run_jobs('python', benchmarks, logger)
    perf_factor = reduce(lambda x, y: x + y['duration'], benchmark_report, 0)

    def scale(file_report):
        return {
            'file_name': file_report['file_name'],
            'weight': file_report['duration'] / perf_factor
        }

    perf_report = map(scale, durations)

    return perf_report

def run_jobs(cmd, schedule, logger):
    duration_report = []

    with futures.ThreadPoolExecutor(max_workers=len(schedule)) as executor:
        proc_futures = [ executor.submit(run_job, cmd, files, logger) for files in schedule ]
        for future in futures.as_completed(proc_futures):
            try:
                duration = future.result()
            except Exception as e:
                print('Exception! %s', e)
            else:
                duration_report.extend(duration)

    return duration_report

def run_job(cmd, file_names, logger):
    """Execute the given command for each of the given files in series. Return
    a 'report' describing the duration and file name of each execution."""
    report = []

    for file_name in file_names:
        start = time.time()

        process = mozprocess.ProcessHandlerMixin(cmd=cmd, args=[file_name])
        write_fn = curry(logger.write_line, process)
        process.processOutputLineHandlers.append(write_fn)
        process.run()
        status = process.wait()

        logger.flush(process)

        if status == 0:
          report.append({
            'file_name': file_name,
            'duration': time.time() - start
          })

    return report
