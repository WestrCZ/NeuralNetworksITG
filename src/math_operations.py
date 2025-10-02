import numpy as np


class MathOperations:
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
    
    def vector_addition (u, v):
        if len(u) != len(v):
            raise ValueError("Vectors must have the same length")
        resultVector = []
        for i in range(len(u)):
            resultVector.append(u[i] + v[i])
        return resultVector