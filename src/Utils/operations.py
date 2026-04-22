from typing import List
import math

#TODO add important parameters/constants to global config

ACTIVATION_FUNCTIONS = ["relu", "sigmoid", "tanh"]

class Operations:
    #vector matrix operations    
    def vector_matrix_product(u: List[float], m: List[List[float]], transpose: bool = False) -> List[float]:
        result = []
        if len(u) != len(m) and not transpose:
            raise Exception(f"Width of vector and height of matrix must be same: Width of vector u: {len(u)}. Height of matrix m: {len(m)}")
        elif len(u) != len(m[0]) and transpose:
            raise Exception(f"Width of vector and width of matrix must be same: Width of vector u: {len(u)} Width of Matrix m: {len(m[0])}")
        if transpose == False:
            for i in range(len(m[0])):
                partialSum = 0
                for j in range(len(m)):  
                    partialSum += u[j] * m[j][i]
                result.append(partialSum)
        else:
            for i in range(len(m)):
                partialSum = 0
                for j in range(len(m[0])):
                    partialSum += u[j] * m[i][j]
                result.append(partialSum)
        return result

    #vector only operations

    def vector_addition(u: List[float], v: List[float]) -> List[float]:
        if len(u) != len(v):
            raise Exception(f"Length of vectors must be the same: Length of u: {len(u)}. Length of v: {len(v)}")
        return [u[i] + v[i] for i in range(len(u))]
        
    #activation functions    
    
    def softmax(u: List[float]) -> List[float]:
        max_val = max(u)
        exp_vals = [math.exp(x - max_val) for x in u]
        sum_exp = sum(exp_vals)
        return [x / sum_exp for x in exp_vals]

    def get_activation(input: float, type: str) -> float:
        if type == "relu":
            return Operations.relu(input)
        elif type == "sigmoid":
            return Operations.sigmoid(input)
        elif type == "tanh":
            return Operations.tanh()    
        raise Exception(f"Activation {type} not implemented")

    def get_activation_derivative(input: float, type: str) -> float:
        if type == "relu":
            return Operations.relu_derivation(input)
        elif type == "sigmoid":
            return Operations.sigmoid_derivation(input)
        elif type == "tanh":
            return Operations.tanh_derivation(input)
        raise Exception(f"Activation {type} not implemented")

    def relu(input: float):
        return max(0, input)
    
    def relu_derivation(input: float):
        return 0 if max(0, input) == 0 else 1 
    
    def sigmoid(input: float):
        return 1 / 1 + math.exp(-input)
    
    def sigmoid_derivation(input: float):
        return input * (1 - input)

    def tanh(input: float):
        return (math.exp(input) - math.exp(-input)) / (math.exp(input) + math.exp(-input))
    
    def tanh_derivation(input: float):
        return 1 - Operations.tanh**2  
    
    #loss function
    
    def cross_entropy(u: List[float], index: int) -> list:#
        eps = 1e-12
        return -math.log(u[index] + eps)
    
    #other operations
    
    def try_parse(data: str) -> int | None:
        try:
            return int(data)
        except:
            return None