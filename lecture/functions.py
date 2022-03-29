import logging

#logging configuration 
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# GCD Euclid algorithm for finding gcd
def gcd_euclid(a: int, b: int) -> int:
    logging.info("gcd_euclid, a: {}, b: {}".format(a, b))
    while True:
        r = a % b
        if r == 0:
            return b
        a = b
        b = r

# Sieve of Eratosthenes for finding primes
def sieve_of_eratosthenes(n: int) -> list:
    logging.info("sieve_of_eratosthenes, n: {}".format(n))
    primes = []
    for i in range(2, n+1):
        primes.append(i)
    for i in range(2, n+1):
        if i in primes:
            for j in range(i*2, n+1, i):
                if j in primes:
                    primes.remove(j)
    return primes

# Sieve of Eratosthenes for finding primes in given range between a and b
def sieve_of_eratosthenes_range(a: int, b: int) -> list:
    logging.info("sieve_of_eratosthenes_range, a: {}, b: {}".format(a, b))
    primes = []
    for i in range(a, b+1):
        primes.append(i)
    for i in range(2, b+1):
        if i in primes:
            for j in range(i*2, b+1, i):
                if j in primes:
                    primes.remove(j)
    return primes

# Produce all mersenne primes smaller than given number n
def mersenne_primes(n: int) -> list:
    logging.info("mersenne_primes, n: {}".format(n))
    
    primes = set(sieve_of_eratosthenes(n))
    mersenne = [2**prime - 1 for prime in primes]
    result = list(primes.intersection(mersenne))
    result.sort()
    return result


def main():
    logging.info("Main")

    logging.info("gcd of 111 and 141: {}".format(gcd_euclid(111, 141)))
    logging.info("primes smaller than 100: {}".format(sieve_of_eratosthenes(100)))
    logging.info("primes greater than 7 and smaller than 100: {}".format(sieve_of_eratosthenes_range(7, 100)))
    logging.info("mersenne primes for n: 1000: {}".format(mersenne_primes(1000)))

if __name__ == "__main__":
    main()