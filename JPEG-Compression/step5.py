import numpy as np
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
sample_array = np.array([
    [75, 1, 0, 0, 0, 0, 0, 0],
    [1, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0]
])
zigzag_result = zigzag_scan(sample_array)
print(", ".join(map(str, zigzag_result)))
