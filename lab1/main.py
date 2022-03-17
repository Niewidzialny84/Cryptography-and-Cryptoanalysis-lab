from asyncio.log import logger
from operator import index
from bitarray import bitarray
from bitarray.util import int2ba
import itertools, os

import logging

#logging configuration 
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

#Reads the file and returns a bitarray
def readFile(fileName: str) -> bitarray:
    logging.info("Reading file: {}".format(fileName))
    bits = bitarray()
    with open(fileName, 'rb') as f:
        bits.fromfile(f)

    size = int(len(bits) / 16)
    logging.info("Bits: {}, Size: {}".format(bits, size))
    return bits, size


#Removes unwanted zeros from the bitarray
def removeZeros(bits: bitarray, size: int) -> bitarray:
    logging.info("Removing zeros")
    for i in range(size):
        for j in range(8):
            bits.pop(8*(i+1))
    logging.info("Bits: {}".format(bits))
    return bits


#Genarate functions based on bitarray
def genarateFunctions(bits: bitarray, size: int) -> list:
    logging.info("Generating functions")
    functions = []
    for i in range(8):
        function = bitarray()
        for j in range(size):
            function.append(bits[i+8*j])
        functions.append(function)
    return functions


#Check function balance based on number of ones and zeros
def checkFunctionBalance(function: bitarray) -> bool:
    logging.info("Checking function balance")
    z = function.count(0)
    o = function.count(1)
    logging.info("Zeros: {}, Ones: {}".format(z, o))
    return z == o


def checkAllFunctionBalance(functions: list):
    logging.info("Checking all functions balance")
    for function in functions:
        if checkFunctionBalance(function) is False:
            logging.info("Function is not balanced [{}]".format(function))


#Create array with all possible combinations of size
def createCombinations(size: int) -> list:
    logging.info("Creating combinations")
    combinations = []
    index = list(range(0, size))
    for i in range(1, size+1):
        combinations += list(itertools.combinations(index, i))
    return combinations


#Genarate linear functions
def genarateLinearFunctions(size: int) -> list:
    logging.info("Generating linear functions")
    functions = []
    for i in range(size):
        function = bitarray('0'*8)
        num = int2ba(i)
        for _ in range(len(str(num.to01()))):
            function.pop()
        function.extend(num)
        functions.append(function)

    combinations = createCombinations(8)

    logger.info("Generating combinations for functions")
    result = []
    for combination in combinations:
        tmp = bitarray()
        for bits in functions:
            xs = []
            for i in combination:
                xs.append(int(bits[7 - i]))
            partResult = xs[0]
            for i in range(1, len(xs), 1):
                partResult ^= xs[i]
            tmp.append(partResult)
        result.append(tmp)

    result.append(bitarray('0'*size))
    return result


#Check functions non-linearity using linear functions
def checkFunctionNonLinearity(functions: bitarray, size: int) -> bool:
    logger.info("Checking function non-linearity of size {}".format(size))
    linearFunctions = genarateLinearFunctions(size)
    result = []
    for function in functions:
        tmpResult = []
        for linearFunction in linearFunctions:
            xor = []
            for i in range(size):
                xor.append(function[i] ^ linearFunction[i])
            tmpResult.append(sum(xor))
        result.append(min(tmpResult))
    return result


#SAC check
def sacCheck(functions: list, size: int) -> list:
    logger.info("SAC check")
    result = []
    for function in functions:
        partResult = []
        for i in range(8):
            newFunction = []
            power = 2**i
            pairNumber = int(size / (power*2))
            lastIndex = 0
            for _ in range(pairNumber):
                up = []
                down = []
                for k in range(lastIndex, lastIndex + power):
                    up.append(int(function[k]))
                    lastIndex += 1
                for k in range(lastIndex, lastIndex + power):
                    down.append(int(function[k]))
                    lastIndex += 1
                newFunction += down + up
            partResult.append(newFunction)
        result.append(partResult)
    
    sacs = []
    for function, partResult in zip(functions, result):
        sac = []
        logger.info("Function: {}".format(function.tobytes().hex()))
        for element in partResult:
            xor = []
            for i in range(size):
                tmpXor = function[i] ^ element[i]
                xor.append(tmpXor)
            sac.append(sum(xor))
        value = (((sum(sac) / len(sac)) / size))
        logger.info("Value: {}".format(value))
        sacs.append(value)
    
    return sacs


def main():          
    logger.info("Starting program")
    file, size = readFile('sbox.SBX')
    file = removeZeros(file, size)

    functions = genarateFunctions(file, size)
    for function in functions:
        logger.info("Function: {}".format(function.tobytes().hex()))

    checkAllFunctionBalance(functions)

    result = checkFunctionNonLinearity(functions, size)
    logger.info("Result Non Linear: {}".format(result))

    sacs = sacCheck(functions, size)
    logger.info("SAC for functions: {}".format(sacs))
    logger.info("Average SAC: {}".format(sum(sacs) / len(sacs)))

if __name__ == '__main__':
    main()