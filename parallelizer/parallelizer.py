import argparse

def cli():
    parser = argparse.ArgumentParser(
                        description="""spawn and benchmark multiple
                        test-running processes""")
    parser.add_argument('-r', '--reporter', default='tap', type=str,
                        choices=['json-stream', 'tbpl', 'tap'],
                        help='The format of the report')
    parser.add_argument('-e', '--exec', required=True, type=str,
                        help='The command to execute')
    parser.add_argument('-t', '--timeout', default=10, type=int,
                        help="""Number of seconds to wait before considering a
                        silent process 'failed' and kiling it""")
    parser.add_argument('files', nargs=argparse.REMAINDER, type=file)
    args = parser.parse_args()

    print 'Hello, world!'

if __name__ == '__main__':
    cli()
