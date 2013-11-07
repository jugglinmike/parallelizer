import argparse

import scheduler
import spawner
from logger import Logger

def main(cmd, files, output):
    logger = Logger(stream=output == 'stream')
    file_names = map(lambda x: x.name, files)
    perf_report = map(lambda x: { 'file_name': x, 'timing': 1 }, file_names)

    schedule = scheduler.make(perf_report, spawner.parallelism())
    perf_report = spawner.spawn(cmd, schedule, logger)
    print perf_report

def cli():
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
    #parser.add_argument('-t', '--timeout', default=10, type=int,
    #                    dest='timeout',
    #                    help="""Number of seconds to wait before considering a
    #                    silent process 'failed' and kiling it""")
    parser.add_argument('files', nargs=argparse.REMAINDER, type=file)

    main(**vars(parser.parse_args()))

if __name__ == '__main__':
    cli()
