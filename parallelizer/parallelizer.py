import argparse
from manifestparser import ManifestParser, ExpressionParser
import mozinfo

import scheduler
import spawner
from reporter import Reporter
from logger import Logger

def files_from_manifest(manifest_file):
    def is_enabled(entry):
        if 'disabled' in entry:
            return False
        if 'run-if' in entry:
            return ExpressionParser(entry['run-if'], vars(mozinfo)).parse()
        if 'skip-if' in entry:
            return not ExpressionParser(entry['skip-if'], vars(mozinfo)).parse()
        return True

    parser = ManifestParser()
    parser.read(manifest_file)
    entries = parser.tests
    entries = filter(is_enabled, parser.tests)
    return map(lambda entry: entry['path'], entries)

def main(cmd, file_names, output, redis_address):
    logger = Logger(stream=output == 'stream')
    reporter = Reporter(**redis_address)

    if len(file_names) == 1:
        file_names = files_from_manifest(file_names[0])

    files = map(file, file_names)

    perf_report = reporter.get_report(files)
    schedule = scheduler.make(perf_report, spawner.parallelism())
    perf_report = spawner.execute(cmd, schedule, logger)

    reporter.submit(perf_report)

def cli():
    def parse_address(address):
        host, port = address.split(':')
        return dict(host=host, port=int(port))

    def verify_file(file_name):
        open(file_name, 'r')
        return file_name

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
    parser.add_argument('file_names', nargs='+', type=verify_file,
                        help="""Test files to run with the given command. If
                        only one file is specified, attempt to parse as a
                        manifest file.""")

    main(**vars(parser.parse_args()))

if __name__ == '__main__':
    cli()
