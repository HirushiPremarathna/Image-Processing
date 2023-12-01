from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import math
input_image = Image.open('images.jpg')
image_array = np.array(input_image)
def rgb_to_ycbcr(pixel):
    y= 16 + 65.738*pixel[0]/256 + 129.057*pixel[1]/256 + 25.064*pixel[2]/256
    cb = 128-37.945*pixel[0]/256 - 74.494*pixel[1]/256 + 112.439*pixel[2]/256
    cr = 128+112.439*pixel[0] - 94.154*pixel[1]/256 - 18.285*pixel[2]/256
    return y, cb, cr
ycbcr_image = np.apply_along_axis(rgb_to_ycbcr, 2, image_array)
y_channel = ycbcr_image[:, :, 0]
cb_channel = ycbcr_image[:, :, 1]
cr_channel = ycbcr_image[:, :, 2]
plt.figure(figsize=(10, 5))
plt.subplot(1, 4, 1)
plt.title("Original Image")
plt.imshow(input_image)
plt.subplot(1, 4, 2)
plt.title("Y Component")
plt.imshow(y_channel, cmap='gray')
plt.subplot(1, 4, 3)
plt.title("Cb Component")
plt.imshow(cb_channel, cmap='gray')
plt.subplot(1, 4, 4)
plt.title("Cr Component")
plt.imshow(cr_channel, cmap='gray')
print(y_channel,y_channel.shape)
print(cb_channel,cb_channel.shape)
print(cr_channel,cr_channel.shape)
plt.show()

# Sample from y_channel is take for next steps.
# Close the plot window to print next steps.

# Step 1: Centering the Matrix
def recenter_matrix(component):
    component = np.array(component)
    centered_matrix = component - 128
    return centered_matrix

# Step 2: Discrete Cosine Transform (DCT)
def dct(component):
    n, m = component.shape
    dct_result = np.zeros((n, m))
    for i in range(m):
        for j in range(n):
            ci = 1 / math.sqrt(m) if i == 0 else math.sqrt(2 / m)
            cj = 1 / math.sqrt(n) if j == 0 else math.sqrt(2 / n)
            sum_dct = 0
            for x in range(m):
                for y in range(n):
                    dct1 = component[x][y] * math.cos((2 * x + 1) * i * np.pi / (2 * m)) * math.cos((2 * y + 1) * j * np.pi / (2 * n))
                    sum_dct += dct1
            dct_result[i][j] = round(ci * cj * sum_dct, 7)
    return dct_result

# Step 3: Quantize DCT Coefficients
def quantize_dct_coefficients(dct_coefficients, quantization_matrix):
    quantized_coefficients = np.round(dct_coefficients / quantization_matrix)
    return quantized_coefficients

luminance_qm = np.array([
    [16, 11, 10, 16, 24, 40, 51, 61],
    [12, 12, 14, 19, 26, 58, 60, 55],
    [14, 13, 16, 24, 40, 57, 69, 56],
    [14, 17, 22, 29, 51, 87, 80, 62],
    [18, 22, 37, 56, 68, 109, 103, 77],
    [24, 35, 55, 64, 81, 104, 113, 92],
    [49, 64, 78, 87, 103, 121, 120, 101],
    [72, 92, 95, 98, 112, 100, 103, 99]
])

# Step 4: Zigzag Scanning
def zigzag_scan(array):
    rows, cols = array.shape
    result = np.zeros(rows * cols, dtype=int)
    i, j = 0, 0
    for k in range(rows * cols):
        result[k] = array[i, j]
        if (i + j) % 2 == 0:  # Moving up
            if i > 0 and j < cols - 1:
                i -= 1
                j += 1
            elif j < cols - 1:
                j += 1
            else:
                i += 1
        else:  # Moving down
            if i < rows - 1 and j > 0:
                i += 1
                j -= 1
            elif i < rows - 1:
                i += 1
            else:
                j += 1
    return result

# Step 6: Run-Length Encoding (RLE)
def rle_encode(data):
    encoded_data = []
    count = 1
    for i in range(1, len(data)):
        if data[i] == data[i - 1]:
            count += 1
        else:
            encoded_data.append((data[i - 1], count))
            count = 1
    encoded_data.append((data[-1], count))
    return encoded_data

# Step 7: Huffman Encoding
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

# Input data for steps 1 to 3
component = np.array([
    [154.12, 154.12, 153.26, 153.26, 152.71, 152.71, 152.71, 151.85],
    [153.26, 153.26, 153.26, 152.40, 152.71, 151.85, 151.85, 151.75],
    [153.26, 152.40, 152.40, 152.40, 151.85, 151.85, 150.89, 150.89],
    [152.40, 151.54, 151.54, 151.85, 150.99, 150.99, 150.03, 150.03],
    [150.99, 150.99, 150.99, 150.13, 150.13, 149.17, 149.17, 149.17],
    [150.13, 150.13, 150.13, 149.27, 149.17, 148.31, 148.31, 148.12],
    [150.03, 149.17, 149.17, 149.17, 148.31, 148.31, 147.26, 147.26],
    [149.17, 149.17, 149.17, 148.31, 148.31, 147.26, 147.26, 147.57]
])

# Execute the steps
centered_matrix = recenter_matrix(component)
dct_matrix = dct(centered_matrix)
quantized_coefficients = quantize_dct_coefficients(dct_matrix, luminance_qm)
zigzag_result = zigzag_scan(quantized_coefficients)
encoded_data = rle_encode(zigzag_result)

# Step 7: Huffman Encoding
freq_table = encoded_data
huffman_root = build_huffman_tree(freq_table)
huffman_encoding = build_huffman_codes(huffman_root)
huffman_encoded_data = encode_with_huffman(freq_table, huffman_encoding)


print("Huffman-encoded data:", huffman_encoded_data)

