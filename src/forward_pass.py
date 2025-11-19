from infrastracture.math_operations import MathOperations as MO
import numpy as np

def forward_pass(input: np.ndarray, model, layer_index = 0) -> np.ndarray: 
    """
    The model has to be formatted to matrices using the ModelShaper.to_matrices() function
    """
    result = np.array([MO.sigmoid(x) for x in MO.vector_addition(MO.matrix_x_vector(model["weights"][layer_index], input), model["biases"][layer_index])])
    layer_index += 1
    if layer_index < len(model["weights"]):
        return forward_pass(result, model, layer_index)
    else:
        return result