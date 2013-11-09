from parallelizer.utils.curry import curry

def curry_test():
    """The created function should curry all original arguments"""

    def get_args(*args):
        return args

    curried = curry(get_args, 1, 2, 3)

    assert(curried(4, 5, 6) == (1, 2, 3, 4, 5, 6))
