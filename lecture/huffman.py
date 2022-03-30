import logging

#logging configuration 
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

class Node:
    def __init__(self, freq: float, symbol: str, left=None, right=None):
        self.freq = freq
        self.symbol = symbol
        self.left = left
        self.right = right
        self.huff = ''

# Huffman coding
def huffman(text: str) -> str:
    # Create frequency table
    freq = {}
    for c in text:
        if c in freq:
            freq[c] += 1
        else:
            freq[c] = 1

    # Create nodes
    nodes = []
    for symbol, freq in freq.items():
        freq = freq / len(text)
        nodes.append(Node(freq, symbol))

    # Create tree and keys based on that
    root = createTree(nodes)
    keys = huffmanKeys(root, {}, '')

    logging.info("Huffman keys: %s", keys)
    
    result = ''
    for c in text:
        result += keys[c]

    return result

def createTree(nodes: list) -> Node:
    while len(nodes) > 1:
        nodes = sorted(nodes, key=lambda x: x.freq)

        left = nodes[0]
        right = nodes[1]

        left.huff = 0
        right.huff = 1

        newNode = Node(left.freq+right.freq, left.symbol+right.symbol ,left, right)

        nodes.remove(left)
        nodes.remove(right)
        nodes.append(newNode)

    return nodes[0]

def huffmanKeys(node: Node, keys: dict, huff: str) -> dict:
    if node.left is None and node.right is None:
        keys[node.symbol] = huff
    else:
        huffmanKeys(node.left, keys, huff+'0')
        huffmanKeys(node.right, keys, huff+'1')
    return keys

class Symbol:
    def __init__(self, symbol: str, freq: float, link: int = None, p: str = None):
        self.symbol = symbol
        self.freq = freq
        self.link = link
        self.p = p

    def __repr__(self) -> str:
        return f"{self.symbol} {self.freq} {self.link} {self.p}"

# Huffman coding using table instead of tree
def huffmanTable(text: str) -> str:
    logging.info("Huffman coding in table")

    # Create frequency table
    freq = {}
    for c in text:
        if c in freq:
            freq[c] += 1
        else:
            freq[c] = 1

    table = []
    for symbol, freq in freq.items():
        freq = freq / len(text)
        table.append(Symbol(symbol, freq))

    # Sort table
    table = sorted(table, key=lambda x: x.freq)    
    charNum = len(table)
    lastLink = 1

    if len(table) == 1:
        table[0].p = 0
    else:
        for i in range(charNum):
            if table[i].p is None:
                i2 = lastLink
                table[i].p = 0
                table[i2].p = 1
                probSum = table[i].freq+table[i2].freq

                lastLink = len(table)
                table[i].link = lastLink
                table[i2].link = lastLink
                table.append(Symbol(None, probSum, 1, lastLink))
        
    logging.info("Huffman table: %s", table)

    codes = {}
    for i in range(len(table)):
        if table[i].symbol is None:
            break
        else:
            code = str(table[i].p)
            index = table[i].link
            while index < len(table)-1:
                code += str(table[index].p)
                index = table[index].link
            codes[table[i].symbol] = code  
    logging.info("Huffman codes: %s", codes)

    result = ''
    for c in text:
        result += codes[c]

    return result

def main():
    logging.info("Main function")

    input_text = 'Hello World!'
    encoded = huffman(input_text)
    logging.info("Orginal:[%s] Encoded: [%s]", input_text, encoded)
    encoded = huffmanTable(input_text)
    logging.info("Orginal:[%s] Encoded: [%s]", input_text, encoded)

if __name__ == "__main__":
    main()