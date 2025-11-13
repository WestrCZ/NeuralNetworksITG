import numpy as np
import random as rnd

INPUT_SIZE = 784
OUTPUT_SIZE = 10
layer_sizes = np.array([INPUT_SIZE, 16, 16, OUTPUT_SIZE])

    #TODO: create better file name
def initialize_parameters(dimensions = (layer_sizes[0], layer_sizes[1], layer_sizes[2], layer_sizes[3])
                          , biases_lower_bound = -10, biases_upper_bound = 10) -> tuple: 
    dimensions[-1] = 10
    weights_length = 0
    biases_length = 0
    weights_delimeters = np.array([0] * (len(dimensions) * 2))
    biases_delimeters = np.array([0] * (len(dimensions) * 2))
    #training_vector = np.array(dimensions[0] * dimensions[1] + dimensions[1] + dimensions[1] * dimensions[2] + dimensions[2] + dimensions[2] * dimensions[3] + dimensions[3]) 
    i = 0
    while i < len(dimensions) - 1:
        #training_vector[i] = np.array([] * (dimensions[i] * dimensions[i + 1])
        delimeter_offset = 2 * i
        weights_delimeters[0 + delimeter_offset] = weights_length
        weights_delimeters[1 + delimeter_offset] = weights_length + dimensions[i] * dimensions[i + 1]
        biases_delimeters[0 + delimeter_offset] = biases_length
        biases_delimeters[1 + delimeter_offset] = biases_length + dimensions[i + 1]
        weights_length += dimensions[i] * dimensions[i + 1]
        biases_length += dimensions[i + 1]
        i += 1
        #for j in range(dimensions[i] * dimensions[i + 1] + dimensions[i + 1]):
            #training_vector[i][j] = rnd.random()
            #training_vector_length

    weights = np.array([rnd.random()] * weights_length)
    biases = np.array([rnd.randint(biases_lower_bound, biases_upper_bound)] * biases_length)
    #TODO: consider changing output to dictionary
    return weights, weights_delimeters, biases, biases_delimeters 

def matrix_structure_convertor(weights, weights_delimeters):
    return
def vector_structure_convertor(weights):
    return