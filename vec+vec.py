import numpy as np

def vector_addition (u, v):
    if len(u) != len(v):
        raise ValueError("Vectors must have the same length")
    resultVector = []
    for i in range(len(u)):
        resultVector.append(u[i] + v[i])
    return resultVector