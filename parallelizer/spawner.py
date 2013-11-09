import os
import re
import subprocess
import time
from concurrent import futures

import mozprocess
from utils import curry

# Source:
# http://stackoverflow.com/questions/1006289/how-to-find-out-the-number-of-cpus-in-python
def parallelism():
    """ Number of available virtual or physical CPUs on this system, i.e.
    user/real as output by time(1) when called with an optimally scaling
    userspace-only program"""

    # cpuset
    # cpuset may restrict the number of *available* processors
    try:
        m = re.search(r'(?m)^Cpus_allowed:\s*(.*)$',
                      open('/proc/self/status').read())
        if m:
            res = bin(int(m.group(1).replace(',', ''), 16)).count('1')
            if res > 0:
                return res
    except IOError:
        pass

    # Python 2.6+
    try:
        import multiprocessing
        return multiprocessing.cpu_count()
    except (ImportError, NotImplementedError):
        pass

    # http://code.google.com/p/psutil/
    try:
        import psutil
        return psutil.NUM_CPUS
    except (ImportError, AttributeError):
        pass

    # POSIX
    try:
        res = int(os.sysconf('SC_NPROCESSORS_ONLN'))

        if res > 0:
            return res
    except (AttributeError, ValueError):
        pass

    # Windows
    try:
        res = int(os.environ['NUMBER_OF_PROCESSORS'])

        if res > 0:
            return res
    except (KeyError, ValueError):
        pass

    # jython
    try:
        from java.lang import Runtime
        runtime = Runtime.getRuntime()
        res = runtime.availableProcessors()
        if res > 0:
            return res
    except ImportError:
        pass

    # BSD
    try:
        sysctl = subprocess.Popen(['sysctl', '-n', 'hw.ncpu'],
                                  stdout=subprocess.PIPE)
        scStdout = sysctl.communicate()[0]
        res = int(scStdout)

        if res > 0:
            return res
    except (OSError, ValueError):
        pass

    # Linux
    try:
        res = open('/proc/cpuinfo').read().count('processor\t:')

        if res > 0:
            return res
    except IOError:
        pass

    # Solaris
    try:
        pseudoDevices = os.listdir('/devices/pseudo/')
        res = 0
        for pd in pseudoDevices:
            if re.match(r'^cpuid@[0-9]+$', pd):
                res += 1

        if res > 0:
            return res
    except OSError:
        pass

    # Other UNIXes (heuristic)
    try:
        try:
            dmesg = open('/var/run/dmesg.boot').read()
        except IOError:
            dmesgProcess = subprocess.Popen(['dmesg'], stdout=subprocess.PIPE)
            dmesg = dmesgProcess.communicate()[0]

        res = 0
        while '\ncpu' + str(res) + ':' in dmesg:
            res += 1

        if res > 0:
            return res
    except OSError:
        pass

    raise Exception('Can not determine number of CPUs on this system')

def execute(cmd, schedule, logger):
    """Asynchronously execute the tests described by the specified command and
    schedule. Return a performance report containing a 'score' for each file
    that terminated normally."""

    durations = run_jobs(cmd, schedule, logger)
    perf_report = make_report(durations)
    return perf_report

def make_report(durations):
    """Given a duration report, create a performance report by normalizing raw
    timing data according to the local system's resources."""
    benchmarks = ['cpu', 'memory', 'disk']
    benchmarks = map(lambda x: ['parallelizer/benchmarks/' + x + '.py'], benchmarks)

    benchmark_report = run_jobs('python', benchmarks)
    perf_factor = reduce(lambda x, y: x + y['duration'], benchmark_report, 0)

    def scale(file_report):
        return {
            'file_name': file_report['file_name'],
            'weight': file_report['duration'] / perf_factor
        }

    perf_report = map(scale, durations)

    return perf_report

def run_jobs(cmd, schedule, logger=None):
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
        if logger:
            process.processOutputLineHandlers.append(curry(logger.write_line, process))
        process.run()
        status = process.wait()

        if logger:
            logger.flush(process)

        if status == 0:
          report.append({
            'file_name': file_name,
            'duration': time.time() - start
          })

    return report
