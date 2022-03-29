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

# Polynomial Euclid algorithm for finding gcd (mod)
def polynomial_gcd_mod(px: list, gx: list, mod: int) -> list:
    logging.info("polynomial_gcd_mod, px: {}, gx: {}, mod: {}".format(px, gx, mod))
    while True:
        qx, rx = pol_div_mod(px, gx, mod)
        l_gx = len(gx)
        l_rx = len(rx)
        if l_rx > 1 and l_gx >= l_rx:
            px = gx
            gx = rx
        else:
            return qx

# Polynomial division (mod)
def pol_div_mod(px: list, gx: list, mod: int) -> list:
    logging.info("pol_div_mod, px: {}, gx: {}, mod: {}".format(px, gx, mod))
    qx = []

    while True:
        power = len(px) - len(gx)
        part_qx = []

        i = 1
        if px[0] % gx[0] == 0:
            i = px[0]/gx[0]
        else:
            while (gx[0] * i) % mod != px[0]:
                i+=1

        part_qx.append(i)
        for i in range(power):
            part_qx.append(0)

        qx = np.polyadd(qx, part_qx)
        qx = [i % mod for i in qx]

        mul = np.polymul(part_qx, gx)
        mul = [i * -1 for i in mul]
        mul = [i % mod for i in mul]

        rx = np.polyadd(px, mul)
        rx = [i % mod for i in rx]
        
        while(len(rx) > 1 and rx[0] == 0):
            rx = rx[1:]

        px = rx
        if len(rx) < len(gx):
            return qx, rx


def main():
    logging.info("Main")

    px = [1, 0, -4, 0, 0, -1, 0, 4]
    gx = [1, -4, -1, 0, 4]

    gcd = polynomial_gcd_mod(px, gx, 2)
    logging.info("gcd: {}".format(gcd))

if __name__ == '__main__':
    main()