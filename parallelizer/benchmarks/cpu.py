def cpu():
    """Calculate a set of prime numbers."""
    def isprime(startnumber):
        startnumber *= 1.0
        for divisor in range(2, int(startnumber**0.5) + 1):
            if startnumber / divisor == int(startnumber / divisor):
                return False
        return True

    for x in xrange(200000):
        isprime(x)

if __name__ == '__main__':
    cpu()
