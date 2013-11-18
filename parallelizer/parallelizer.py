import argparse
import sys

import scheduler
import spawner
from reporter import Reporter
from logger import Logger

def reduce_perf_report(current_status, file_report):
    """Reduce a perf report describing many exit status to a single number: 0 if
    all were zero, and 1 if one or more were non-zero"""
    return 1 & current_status | (file_report['status'] != 0)

def main(cmd, files, output, redis_address):
    logger = Logger(stream=output == 'stream')
    reporter = Reporter(**redis_address)

    perf_report = reporter.get_report(files)
    schedule = scheduler.make(perf_report, spawner.parallelism())
    perf_report = spawner.execute(cmd, schedule, logger)

    reporter.submit(perf_report)

    status_code = reduce(reduce_perf_report, perf_report, 0)
    sys.exit(status_code)

def cli():
    def parse_address(address):
        host, port = address.split(':')
        return dict(host=host, port=int(port))

    parser = argparse.ArgumentParser(
                        description="""spawn and benchmark multiple
                        test-running processes""")
    #parser.add_argument('-r', '--reporter', default='tap', type=str,
    #                    choices=['json-stream', 'tbpl', 'tap'],
    #                    dest='reporter', help='The format of the report')
    parser.add_argument('-c', '--cmd', required=True, type=str,
                        dest='cmd', help='The command to execute')
    parser.add_argument('-o', '--output', type=str, default='stream',
                        dest='output', choices=['stream', 'buffer'],
                        help="""Method for logging output of interleaved
                        processes""")
    parser.add_argument('-r', '--redis', type=parse_address,
                        dest='redis_address', default='localhost:6379',
                        help="""The address of the Redis-powered performance
                        database""")
    #parser.add_argument('-t', '--timeout', default=10, type=int,
    #                    dest='timeout',
    #                    help="""Number of seconds to wait before considering a
    #                    silent process 'failed' and kiling it""")
    parser.add_argument('files', nargs=argparse.REMAINDER, type=file)

    main(**vars(parser.parse_args()))

if __name__ == '__main__':
    cli()
