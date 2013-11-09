def curry(target, *bound):
    """Given a "target" function and an arbitrary list of "bound" positional
    arguments, create a function that invokes the "target" function with the
    "bound" arguments along with any additionally-specified arguments."""
    return lambda *args: target(*(bound + args))
