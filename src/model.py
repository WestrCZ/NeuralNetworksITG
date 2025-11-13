import math
import numpy as np

class model:
    def init(self):
        INPUT_SIZE = 729
        OUTPUT_SIZE = 10
        layer_sizes = []
        weights_vector = []
        weights_matrix = []
        biases_vector = []
        biases_matrix = []

        layer_sizes.append(INPUT_SIZE)
        layer_sizes.extend(self.inputLayers())
        layer_sizes.append(OUTPUT_SIZE)

        weights_vector,weights_matrix,biases_vector,biases_matrix = self.createWeightsAndBiases(layer_sizes)

    def inputLayers():
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

    def createWeightsAndBiases(layers):
        weights_vectored = []
        biases_vectored = []

        weights_matrixed = []
        biases_matrixed = []

        for i in range(len(layers)-1): 
            input_size = layers[i]
            output_size = layers[i + 1]
            weight_matrix = []
            bias_matrix = []

            for j in range(layers[i]*layers[i+1]):
                # TODO: Consider Xavier initialization
                randNum = np.random.uniform(-1, 1)
                weights_vectored.append(randNum)
                weight_matrix.append(randNum)

            for j in range(layers[i+1]):
                # Biases tend to be initialized at 0.0
                biases_vectored.append(0.0)
                bias_matrix.append(0.0)

            weights_matrixed.append(np.array(weight_matrix).reshape(input_size,output_size))
            biases_matrixed.append(np.array(bias_matrix).reshape(output_size))

        return weights_vectored, weights_matrixed, biases_vectored, biases_matrixed

    def laodTrainedModel(self, path):
        from json_loader import json_loader
        structure, weights, biases = json_loader(path)
        return structure, weights, biases
    
    if __name__ == "__main__":
        init()
