import numpy as np

def matrixvector_multiplication(matrix, vector):
    M = np.array(matrix)
    v = np.array(vector)

    rowsM, colsM = M.shape
    if colsM != v.shape[0]:
        raise ValueError("Length is not compatible")

    result = []
    for i in range(rowsM):
        partialSum = 0
        for j in range(colsM):
            partialSum += M[i][j] * v[j]
        result.append(partialSum)
    return result