class Logger(object):
    """Control the output of multiple processes."""
    def __init__(self, stream=True):
        self._buffers = {}
        self.stream = stream
        pass

    def write_line(self, process, line):
        """Forward the provided line of output to standard out or store it in
        a per-process buffer."""
        if self.stream:
            print line
            return

        if process not in self._buffers:
          self._buffers[process] = []

        self._buffers[process].append(line)

    def flush(self, process):
        """Print all buffered output from a given process to standard out."""
        if self.stream or process not in self._buffers:
            return

        for line in self._buffers[process]:
            print line

        del self._buffers[process]
