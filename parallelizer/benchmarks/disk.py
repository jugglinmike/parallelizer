from tempfile import TemporaryFile

def disk():
    """Write dummy data to a temporary file."""
    f = TemporaryFile()
    buf = '0' * 1023 + '\n'
    for _ in xrange(10):
        for _ in xrange(1024 * 8):
            f.write(buf)
        f.seek(0)
        while f.readline():
            pass

    f.close()

if __name__ == '__main__':
    disk()
