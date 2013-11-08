def memory():
    """Write and re-write dummy data to an in-memory dictionary."""
    data = dict()
    buf = '0' * 1024
    for _ in xrange(80):
        for y in xrange(300000):
          data[y] = y

if __name__ == '__main__':
    memory()
