import numpy as np

import logging

#logging configuration 
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

"""
Polynomial in array form:
[an, an-1, ..., a0]
equals
an*x^n + an-1*x^(n-1) + ... + a0
"""

# Polynomial Euclid algorithm for finding gcd
def polynomial_gcd(px: list, gx: list) -> list:
    logging.info("polynomial_gcd, px: {}, gx: {}".format(px, gx))
    
    qx, rx = polynomial_division(px, gx)
    while True:
        qx, rx = polynomial_division(px, gx)
        l_gx = len(gx)
        l_rx = len(rx)
        if l_rx > 1 and l_gx >= l_rx:
            px = gx
            gx = rx
        else:
            return gx

# Polynomial division
def polynomial_division(px: list, gx: list) -> list:
    logging.info("polynomial_division, px: {}, gx: {}".format(px, gx))

    qx = []

    while True:
        power = len(px) - len(gx)
        part_qx = []
        part_qx.append(px[0]/gx[0])
        for i in range(power):
            part_qx.append(0)

        qx = np.polyadd(qx, part_qx)

        mul = np.polymul(part_qx, gx)
        mul = [i * -1 for i in mul]

        rx = np.polyadd(px, mul)
        while(len(rx) > 1 and rx[0] == 0):
            rx = rx[1:]

        px = rx
        if len(rx) < len(gx):
            logging.info("qx: {} rx: {}".format(qx,rx))
            return qx, rx


def main():
    logging.info("Main")

    px = [1, 0, 1, 0, -3, -3, 8, 2, -5]
    gx = [3, 0, 5, 0, -4, -9, 21]

    gcd = polynomial_gcd(px, gx)
    logging.info("gcd: {}".format(gcd))


if __name__ == '__main__':
    main()