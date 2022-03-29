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

def main():
    logging.info("Main function")

    input_text = 'Hello World!'
    encoded = huffman(input_text)
    logging.info("Orginal:[%s] Encoded: [%s]", input_text, encoded)

if __name__ == "__main__":
    main()