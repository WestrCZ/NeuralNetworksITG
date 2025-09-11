import math
import numpy as np

def init():
    INPUT_SIZE = 729
    OUTPUT_SIZE = 10
    layer_sizes = []
    weights = []
    biases = []

    layer_sizes.append(INPUT_SIZE)
    
    # TODO: Případně vymazat idk, to je na vás. Dlouho jsem na to nekoukal.
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

    layer_sizes.append(OUTPUT_SIZE)
    print("layer_sizes:", layer_sizes)

    for i in range(len(layer_sizes)-1): 
        input_size = layer_sizes[i]
        output_size = layer_sizes[i + 1]
        weight_matrix = []
        bias_matrix = []

        for j in range(layer_sizes[i]*layer_sizes[i+1]):
            weight_matrix.append(np.random.rand())

        for j in range(layer_sizes[i+1]):
            bias_matrix.append(np.random.rand())

        biases.append(np.array(bias_matrix).reshape(layer_sizes[i+1]))
        weights.append(np.array(weight_matrix).reshape(layer_sizes[i],layer_sizes[i+1]))

    print("Weight shapes:")
    for w in weights:
        print(f"Weights: {w}")

    for b in biases:
        print(f"Biases: {b}")

def sigmoid(x):
    return 1 / (1 + math.exp(-x))

if __name__ == "__main__":
    init()
