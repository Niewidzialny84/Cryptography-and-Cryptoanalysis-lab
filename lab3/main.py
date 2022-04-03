from asyncio.log import logger
import logging
from math import log2

#logging configuration 
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

import numpy as np
from bitarray import bitarray

# Sha-3 algorithm
class SHA3():
    # Initialize the class
    def __init__(self) -> None:
        logging.info("Initializing SHA3 class")

        pass
        
    # Convert S[w*(5y+x)+z] bitarray to A[x,y,z] numpy array
    def __convert_to_A(self, S: np.ndarray, w: int) -> np.ndarray:
        logging.info("Converting to A")
        A = np.zeros((5, 5, w), dtype=np.uint8)
        for x in range(5):
            for y in range(5):
                for z in range(w):
                    A[x, y, z] = S[w*(5*y+x)+z]
        return A

    # Convert A[x,y,z] numpy array to S[w*(5y+x)+z] bitarray
    def __convert_to_S(self, A: np.ndarray, w: int) -> bitarray:
        logging.info("Converting to S")
        S = bitarray()
        for x in range(5):
            for y in range(5):
                for z in range(w):
                    S.append(A[x, y, z])
        return S

    # Keccak theta function
    def __theta(self, A: np.ndarray, w: int) -> np.ndarray:
        logging.info("Theta function")
        
        # Create C[x,z] = A[x,0,z] ^ A[x,1,z] ^ A[x,2,z] ^ A[x,3,z] ^ A[x,4,z] numpy array 
        C = np.zeros((5, w), dtype=np.uint8)
        for x in range(5):
            for z in range(w):
                C[x, z] = A[x, 0, z] ^ A[x, 1, z] ^ A[x, 2, z] ^ A[x, 3, z] ^ A[x, 4, z]
        
        # Create D[x,z] = C[(x-1)%5,z] ^ C[(x+1)%5,(z-1)%w] numpy array
        D = np.zeros((5, w), dtype=np.uint8)
        for x in range(5):
            for z in range(w):
                D[x, z] = C[(x-1)%5, z] ^ C[(x+1)%5, (z-1)%w]
        
        # Create A'[x,y,z] = A[x,y,z] ^ D[x,z] numpy array
        A_prime = np.zeros((5, 5, w), dtype=np.uint8)
        for x in range(5):
            for y in range(5):
                for z in range(w):
                    A_prime[x, y, z] = A[x, y, z] ^ D[x, z]
        
        return A_prime

    # Keccak rho function
    def __rho(self, A: np.ndarray, w: int) -> np.ndarray:
        logging.info("Rho function")
        
        # Create A'[x,y,z] numpy array using algorithm
        # For all z such that 0 <= z < w let A'[0,0,z] = A[0,0,z]
        # Let (x,y) = (1,0)
        # For t from 0 to 23:
        #     for all z such that 0 <= z < w let A'[x,y,z] = = A[x,y,(z-(t+1)(t+2))]
        #     Let (x,y) = (y, (2*x+3*y)%5)

        A_prime = np.zeros((5, 5, w), dtype=np.uint8)
        A_prime[0, 0, :] = A[0, 0, :]
        x ,y = 1, 0
        for t in range(24):
            for z in range(w):
                A_prime[x, y, z] = A[x, y, (z-(t+1)*(t+2))%w]
            x, y = y, (2*x+3*y)%5

        return A_prime

    # Keccak pi function
    def __pi(self, A: np.ndarray, w: int) -> np.ndarray:
        logging.info("Pi function")

        # For all triplets (x,y,z) such that 0 <= x < 5 and 0 <= y < 5 and 0 <= z < w let A'[x,y,z] = A[(x+3y)%5,x,z])]
        A_prime = np.zeros((5, 5, w), dtype=np.uint8)
        for x in range(5):
            for y in range(5):
                for z in range(w):
                    A_prime[x, y, z] = A[(x+3*y)%5, x, z]

        return A_prime
    
    # Keccak chi function
    def __chi(self, A: np.ndarray, w: int) -> np.ndarray:
        logging.info("Chi function")

        # For all triplets (x,y,z) such that 0 <= x < 5 and 0 <= y < 5 and 0 <= z < w let A'[x,y,z] = A[x,y,z] ^ ((~A[(x+1)%5,y,z]) & A[(x+2)%5,y,z])
        A_prime = np.zeros((5, 5, w), dtype=np.uint8)
        for x in range(5):
            for y in range(5):
                for z in range(w):
                    A_prime[x, y, z] = A[x, y, z] ^ ((~A[(x+1)%5, y, z]) & A[(x+2)%5, y, z])

        return A_prime

    # Keccak iota function
    def __iota(self, A: np.ndarray, w: int, i: int) -> np.ndarray:
        logging.info("Iota function")

        # For all triplets (x,y,z) such that 0 <= x < 5 and 0 <= y < 5 and 0 <= z < w let A'[x,y,z] = A[x,y,z]
        # Let RC = 0^w
        # For j from 0 to  l let RC[(2**j) - 1] = rc(j+(7*i))
        # For all z such that 0 <= z < w let A'[0,0,z] = A[0,0,z] ^ RC[z]

        A_prime = np.zeros((5, 5, w), dtype=np.uint8)
        for x in range(5):
            for y in range(5):
                for z in range(w):
                    A_prime[x, y, z] = A[x, y, z]

        # rc(t) is computed as follows:
        # If t mod 255 == 0 then rc[t] = 1
        # Let R = 10000000
        # For i from 1 to t mod 255, let:
        #     R = 0 || R
        #     R[0] = R[0] ^ R[8]
        #     R[4] = R[4] ^ R[8]
        #     R[5] = R[5] ^ R[8]
        #     R[6] = R[6] ^ R[8]
        #     R = Trunc8[R]
        # return R[0]
        def rc(t: int) -> int:
            if t % 255 == 0:
                return 1
            R = bitarray('10000000')
            for i in range(t % 255):
                R.append(False)
                R[0] = R[0] ^ R[8]
                R[4] = R[4] ^ R[8]
                R[5] = R[5] ^ R[8]
                R[6] = R[6] ^ R[8]
                R = R[:8]
            return R[0]

        RC = np.zeros(w, dtype=np.uint8)
        for j in range(int(log2(w))):
            RC[(2**j) - 1] = rc(j+(7*i))
        
        A_prime[0, 0, :] = A[0, 0, :] ^ RC  

        return A_prime

    # Keccak-p function for string S - Keccak-p[b,nr](S)
    def __keccak_p(self, b: int, nr: int, S: str) -> bitarray:
        logging.info("Keccap-p function")

        w = int(b/25)

        logging.info("b = %d, nr = %d, w = %d", b, nr, w)

        # Convert string S to a numpy array A
        A = self.__convert_to_A(S, w)

        # Initialize A' to A
        A_prime = A

        # For i from 0 to nr - 1:
        #     A = Keccak-p[b,nr](A)
        for ir in range(nr):
            logger.info("Iteration Keccak %d", ir)

            A_prime = self.__theta(A, w)
            A_prime = self.__rho(A_prime, w)
            A_prime = self.__pi(A_prime, w)
            A_prime = self.__chi(A_prime, w)
            A_prime = self.__iota(A_prime, w, ir)

        # Convert A_prime to a string S'
        S_prime = self.__convert_to_S(A_prime,w)

        return S_prime

    # Keccak[c] using Sponge construction
    def __sponge(self, N: bitarray, c: int = 512, f: list = [1600,24], d: int = 256) -> bitarray:
        logging.info("Sponge construction")

        # In the sponge construction the message N is padded to P such that length(P) is a multiple of r
        # Each block of P of length r is then “absorbed” by the sponge by padding it with 0c and XORing it with the current state
        # Let P = N || pad(r,len(N))
        # Let n = len(P)/r
        # Let c = b-r
        # Let P[0], ... P[n-1] be the unique sequence of strings of length r such that P = P[0] || ... || P[n-1]
        # Let S=0**b
        # For i from 0 to n-1: let S=f(S^(P[i] || 0**c))
        # Let Z be the empty string
        # Let Z = Z || Trunc(S,r)
        # If d <= |Z| then return Trunc(Z,d); else continue
        # Let S = f(S), and continue with step 8

        b, nr = f[0], f[1]

        # Pad N to P
        P = N.copy()
        r = b - c
        pad = (r - (len(P) % r) - 2)
        logging.info("pad = %d, N-len = %d, r = %d", pad, len(N), r)
        P.extend(bitarray('1' + '0'*pad + '1'))

        # Calculate n
        n = len(P) // r
        logging.info("n = %d", n)
        Pi = []
        for i in range(n):
            Pi.append(P[i*r:(i+1)*r])

        S = bitarray('0'*b)
        for i in range(n):
            Pi[i].extend(bitarray('0'*c))
            S = self.__keccak_p(b, nr, S ^ Pi[i])
        
        Z = bitarray('0'*r)
        
        while len(Z) < d:
            S = self.__keccak_p(b, nr, S)
            Z = Z ^ S[:r]

        return Z[:d]
    
    # Sha 3-256 execution
    @staticmethod
    def sha3_256(message: str) -> str:
        logging.info("Executing sha3-256 on message: {}".format(message))
        
        # Initialize class
        sha3 = SHA3()
        
        # Convert string message to bitarray
        N = bitarray()
        N.frombytes(message.encode('utf-8'))
       
        # Execute Sponge construction
        bits = sha3.__sponge(N)

        # Convert bitarray to hexadecimal string
        return bits.to01()

def main():
    logging.info("Main")
    
    message = "Hello World!"
    logging.info("Message: {}".format(message))
    result = SHA3.sha3_256(message)
    logging.info("Result: {}".format(result))

if __name__ == "__main__":
    main()