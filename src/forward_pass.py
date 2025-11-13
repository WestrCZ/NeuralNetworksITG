from model import model
from math_operations import MathOperations
import numpy as np

def forward_pass(model, activations):
    math_ops = MathOperations()
    
    weights_start = 0
    weights_end = 0
    biases_start = 0
    biases_end = 0
    
    for layer_index in range(len(model.layer_sizes) - 1):
        weights_end += model.layer_sizes[layer_index] * model.layer_sizes[layer_index + 1]
        biases_end += model.layer_sizes[layer_index + 1]
        #TODO: Calculation
        
        print(f"Weights: [{weights_start}:{weights_end}]")
        print(f"Biases: [{biases_start}:{biases_end}]")
        weights_start = weights_end
        biases_start = biases_end        
    return activations

    # Example usage:
    # model_instance = model()
    # model_instance.layer_sizes = [784, 16, 16, 10]
    # model_instance.weights_vector = [...]  # Fill with appropriate weights
    # model_instance.biases_vector = [...]   # Fill with appropriate biases
    # input_data = [...]  # Fill with appropriate input data
    # output = forward_pass(model_instance, input_data)
    # print("Output of the forward pass:", output)
    
    



        
# for layer_index in range(len(model.layer_sizes) - 1):
#     weights_start = sum(model.layer_sizes[i] * model.layer_sizes[i + 1] for i in range(layer_index))
#     weights_end = weights_start + model.layer_sizes[layer_index] * model.layer_sizes[layer_index + 1]
#     biases_start = sum(model.layer_sizes[i + 1] for i in range(layer_index))
#     biases_end = biases_start + model.layer_sizes[layer_index + 1]
#     weights_matrix = np.array(model.weights_vector[weights_start:weights_end]).reshape((model.layer_sizes[layer_index + 1], model.layer_sizes[layer_index]))
#     biases_vector = np.array(model.biases_vector[biases_start:biases_end])
#     # Matrix-vector multiplication
#     z = math_ops.matrixvector_multiplication(weights_matrix, activations)
#     # Adding biases
#     z = math_ops.vector_addition(z, biases_vector)
#     # Applying activation function (sigmoid)
#     activations = [math_ops.sigmoid(val) for val in z]
# return activations
        