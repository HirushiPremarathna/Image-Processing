import numpy as np
import math
def dct(component):
    n, m = 8, 8
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
component = np.array([
    [26.12, 26.12, 25.26, 25.26, 24.71, 24.71, 24.71, 23.85],
    [25.26, 25.26, 25.26, 24.4, 24.71, 23.85, 23.85, 23.75],
    [25.26, 24.4, 24.4, 24.4, 23.85, 23.85, 22.89, 22.89],
    [24.4, 23.54, 23.54, 23.85, 22.99, 22.99, 22.03, 22.03],
    [22.99, 22.99, 22.99, 22.13, 22.13, 21.17, 21.17, 21.17],
    [22.13, 22.13, 22.13, 21.27, 21.17, 20.31, 20.31, 20.12],
    [22.03, 21.17, 21.17, 21.17, 20.31, 20.31, 19.26, 19.26],
    [21.17, 21.17, 21.17, 20.31, 20.31, 19.26, 19.26, 19.57]
])
dct_matrix = dct(component)
np.set_printoptions(precision=7, suppress=True)
print(dct_matrix)
