import numpy as np

class MathOperations: # in the future remove all exception raising
    def matrix_x_vector(matrix, vector):
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
    
    def factorial(n):
        fact = 1
        for i in range(1, n + 1):
            fact *= i
        return fact
    def taylor(x):
        e = 0
        for i in range(10): # accuracy - keep the number even
            e += x**i/MathOperations.factorial(i)
        return e
    def sigmoid(x): # 5 digit accuracy
        if(x >= 0):
            return 1-1/(MathOperations.taylor(x)+1)
        else:
            return 1/(MathOperations.taylor(-x)+1)
    def cost_function(answer_vector, correct_vector):
        """
        answer_vector (forward pass): last layer of results (0-9) where for example [0.1, 0.45, ...], uncorrected result of nn, correct_vector: ideal anwser (pure 1)
        """
        if (len(answer_vector) == len(correct_vector)):
            result = 0
            for i in range(len(answer_vector)):
                difference = correct_vector[i] - answer_vector[i]
                result += difference * difference
            return result
        return ValueError