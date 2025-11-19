from forward_pass import forward_pass as fp
from json_loader import json_loader as jl
import numpy as np

class model:    
    def __init__(self):
        self.weights_vector = []
        self.weights_matrix = []
        self.biases_vector = []
        self.biases_matrix = []
        self.layer_sizes = []
        self.init()

    def init(self):
        INPUT_SIZE = 729
        OUTPUT_SIZE = 10
        layer_sizes = []
    
        layer_sizes.append(INPUT_SIZE)
        layer_sizes.extend(self.inputLayers())
        layer_sizes.append(OUTPUT_SIZE)
    
        weights_vector, weights_matrix, biases_vector, biases_matrix = self.createWeightsAndBiases(layer_sizes)
        self.weights_vector = weights_vector
        self.weights_matrix = weights_matrix
        self.biases_vector = biases_vector
        self.biases_matrix = biases_matrix
        self.layer_sizes = layer_sizes

    def inputLayers(self):
        layer_sizes = []
        i = 0
        while True:
            print(f"How many nodes should layer {i+1} have?")
            inputed_layer = input()
            if inputed_layer.isnumeric():
                if int(inputed_layer) > 0:
                    i += 1
                    layer_sizes.append(int(inputed_layer))
                else:
                    break
            else:
                print("Please enter a valid positive integer or 0 to stop.")

        print("layer_sizes:", layer_sizes)
        return layer_sizes

    def createWeightsAndBiases(self, layers):
        weights_vectored = []
        biases_vectored = []
        weights_matrixed = []
        biases_matrixed = []
    
        for i in range(len(layers) - 1):
            input_size = layers[i]
            output_size = layers[i + 1]
            weight_matrix = np.random.uniform(-1, 1, (input_size, output_size))
            bias_matrix = np.zeros(output_size)
    
            weights_vectored.extend(weight_matrix.flatten())
            biases_vectored.extend(bias_matrix)
            weights_matrixed.append(weight_matrix)
            biases_matrixed.append(bias_matrix)

        return weights_vectored, weights_matrixed, biases_vectored, biases_matrixed

if __name__ == "__main__":
    model_instance = model()
    structure, weights, biases = jl("./models/trained.model.json")

    # Example call — replace with real MNIST input later
    dummy_input = np.random.rand(4, 1)
    result = fp(model_instance, dummy_input)

    print("Forward pass result:", result)