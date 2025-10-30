import numpy as np
import random as rnd

#TODO: create better file name and better class name
class operator_iniatilizer():

    INPUT_SIZE = 784
    OUTPUT_SIZE = 10
    LAYER_SIZES = np.array([INPUT_SIZE, 16, 16, OUTPUT_SIZE])

    def initialize_parameters(dimensions = np.array(LAYER_SIZES[0], LAYER_SIZES[1], LAYER_SIZES[2], LAYER_SIZES[3])
                            , biases_lower_bound = -10, biases_upper_bound = 10) -> tuple: 
        dimensions[-1] = 10
        weights_length = 0
        biases_length = 0
        weights_delimeters = np.empty(len(dimensions) * 2, dtype=int)
        biases_delimeters = np.empty(len(dimensions) * 2, dtype=int)
        #weights_delimeters = np.array([0] * (len(dimensions) * 2))
        #biases_delimeters = np.array([0] * (len(dimensions) * 2))
        #training_vector = np.array(dimensions[0] * dimensions[1] + dimensions[1] + dimensions[1] * dimensions[2] +  dimensions[2] + dimensions[2] * dimensions[3] + dimensions[3]) 
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

    def matrix_structure_convertor(weights: np.ndarray, weights_delimeters: np.ndarray, dimensions: np.ndarray):
        weights_array = np.empty(dimensions, dtype=np.ndarray)
        weights_index = 0
        for i in range(len(dimensions) - 1):
            weights_array[i] = np.empty(dimensions[i + 1], dtype=float)
            for _ in dimensions[i]:
                for j in range(dimensions[i + 1]):
                    weights_array[i][j] = weights[weights_index]
                    weights_index += 1 
            
    def vector_structure_convertor(weights: np.ndarray):
        