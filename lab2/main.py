import re, os
from typing import Tuple

import logging

#logging configuration 
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

class Sbox:
    def __init__(self, number: int, array: list):
        logging.info("Initializing Sbox")
        
        self.number = number
        self.array = array
        
        self.createDirectory()

    def getValueAtSi(self, place: int) -> int:
        binary = format(place, "06b")
        r = ""+str(binary[0]) + str(binary[5])
        c = ""+str(binary[1]) + str(binary[2]) + str(binary[3]) + str(binary[4])
        return self.array[int(r, 2)][int(c, 2)]

    def createDirectory(self):
        if not os.path.exists(self.getSboxName()):
            os.makedirs(self.getSboxName())

    def getSboxName(self) -> str:
        return 'SBOX' + str(self.number)

    def saveInDirectory(self, fileName: str, data: str):
        with open(self.getSboxName() + '/' + fileName + '.txt', 'w') as f:
            f.write(data)

    def __str__(self):
        return self.getSboxName() + '\n' + '\n'.join(' '.join(str(x) for x in y) for y in self.array)

    def __repr__(self):
        return str(self)

#Reads the file and returns a list of Sbox
def readSbox(fileName: str) -> list:
    logging.info("Reading Sbox")
    result = []
    with open(fileName, 'r') as f:
        file = f.readlines()
    
    size = int(len(file) / 5)
    for i in range(size):
        sbox = []
        for j in range(1, 5):
            line = file[i*5+j]
            sbox.append([int(s) for s in re.findall(r'\b\d+\b', line)])
        result.append(Sbox(i+1,sbox))
    return result

#Generate TDR and TZP tables for sbox
def generateTables(sbox: Sbox) -> Tuple[list, list] :
    logging.info("Generating tables")

    tdr, tzp = [], []
    for i in range(64):
        tdr.append(list(0 for j in range(16)))
        tzp.append(list(list() for j in range(16)))

    for x1 in range(64):
        for x2 in range(64):
            so = x1 ^ x2
            y1 = sbox.getValueAtSi(x1)
            y2 = sbox.getValueAtSi(x2)
            si = y1 ^ y2
            tdr[so][si] += 1
            tzp[so][si].append((x1, x2))

    with open(sbox.getSboxName() + '/TDR.txt', 'w') as f:
        for i in range(64):
            f.write(str(tdr[i]) + '\n')
    
    with open(sbox.getSboxName() + '/TZP.txt', 'w') as f:
        for i in range(64):
            f.write(str(tzp[i]) + '\n')

    return tdr, tzp

# Highest pair indexes 
def highestPairIndexes(tdr: list, n: int) -> list:
    logging.info("Getting highest pair indexes")
    hV = [0] * n
    hI = [(0, 0)] * n

    for i in range(n):
        for j in range(len(tdr)):
            row = tdr[j]
            highest = max(row)
            if highest != 64:
                for k in range(n):
                    if hV[k] < highest and (j, row.index(highest)) not in hI:
                        hI[k] = (j, row.index(highest))
                        hV[k] = highest
                        break
    return hI

# Function for pair (x1, x2) based on tzp table
def pairFromIndex(tzp: list, row: list) -> list:
    logging.info("Getting pair from index")
    pair = []

    for r in row:
        pair.append(tzp[r[0]][r[1]])
    return pair

# Creates keys based on pair and row
def getKeys(pair: list, row: list) -> dict:
    logging.info("Getting keys")
    keys = []

    for r, c in zip(pair, row):
        for p in r:
            x1, x2 = 1, 0
            while x1 ^ x2 != c[0]:
                x2 += 1
            keys.append(p[0] ^ x1)
    
    result = dict()
    for key in keys:
        if key in result:
            result[key] += 1
        else:
            result[key] = 1
    
    return dict(sorted(result.items(), key=lambda x: x[1], reverse=True))
    
# Gets n best keys from given keys dictionary
def getNBestKeys(keys: dict, n: int) -> dict:
    logging.info("Getting n best keys")
    result = dict()
    i = 0
    for key in keys.items():
        if i < n:
            result[hex(key[0])] = key[1]
            i += 1
    
    return result

#Main function
def main():
    logging.info("Starting main")

    sboxes = readSbox('sboxes.txt')
    for sbox in sboxes:
        logging.info(sbox)

        tdr, tzp = generateTables(sbox)

        row = highestPairIndexes(tdr, 16)
        sbox.saveInDirectory('HPI', str(row))

        pair = pairFromIndex(tzp, row)
        sbox.saveInDirectory('PFI', str(pair))

        keys = getKeys(pair, row)
        sbox.saveInDirectory('KEYS', str(keys))

        bestKeys = getNBestKeys(keys, 5)
        sbox.saveInDirectory('BESTKEYS', str(bestKeys))


if __name__ == "__main__":
    main()