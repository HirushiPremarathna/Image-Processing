class Node:
    def __init__(self, symbol, frequency):
        self.symbol = symbol
        self.frequency = frequency
        self.left = None
        self.right = None
def build_huffman_tree(freq_table):
    nodes = [Node(symbol, freq) for symbol, freq in freq_table]
    while len(nodes) > 1:
        nodes.sort(key=lambda node: node.frequency)
        left = nodes.pop(0)
        right = nodes.pop(0)
        parent = Node(None, left.frequency + right.frequency)
        parent.left = left
        parent.right = right
        nodes.append(parent)
    return nodes[0]
def build_huffman_codes(root, prefix="", code={}):
    if root:
        if root.symbol is not None:
            code[root.symbol] = prefix
        build_huffman_codes(root.left, prefix + "0", code)
        build_huffman_codes(root.right, prefix + "1", code)
    return code
def encode_with_huffman(data, encoding_table):
    encoded_data = ""
    for symbol, freq in data:
        encoded_data += encoding_table[symbol] * freq
    return encoded_data
rle_data = [(75, 1), (1, 2), (0, 61)]
freq_table = rle_data
huffman_root = build_huffman_tree(freq_table)
huffman_encoding = build_huffman_codes(huffman_root)
encoded_data = encode_with_huffman(rle_data, huffman_encoding)
print("Huffman-encoded data:", encoded_data)