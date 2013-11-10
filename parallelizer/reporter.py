import hashlib
import redis
import operator

TIME_TO_LIVE = 30

def hash_file(handle):
    return hashlib.sha1(handle.read()).hexdigest()

class Reporter(object):
    def __init__(self, host, port, db=0):
        self.redis = redis.StrictRedis(host=host, port=port, db=db)

    def get_report(self, files):
        file_names = map(lambda x: x.name, files)
        hashes = map(hash_file, files)
        weights = self.redis.mget(*hashes)

        # For files that are unrecognized by the server, estimate the weight as
        # the average of the weights of the recognized files.
        known_weights = map(float, filter(lambda x: x, weights))
        avg_weight = sum(known_weights) / float(len(known_weights) or 1) or 1
        weights = map(lambda x: x or avg_weight, weights)

        perf_report = map(
            lambda x: dict(file_name=x[0], weight=float(x[1])),
            zip(file_names, weights)
        )
        return perf_report

    def submit(self, report):
        if len(report) == 0:
            return

        pipe = self.redis.pipeline()
        key_vals = dict()
        for file_report in report:
            key = hash_file(file(file_report['file_name']))
            key_vals[key] = file_report['weight']
            pipe.setex(key, TIME_TO_LIVE, file_report['weight'])

        return pipe.execute()
