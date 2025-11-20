from forward_pass import forward_pass as fp
from infrastructure.model_shaper import ModelShaper as MS
from infrastructure.file_manager import FileManager as FM
import numpy as np

class model:    
    def __init__(self):
        print("Dev version started")
        model = {}
        while True:
            inner_layers = []
            bias_spread = []
            print("Please input whether you want to create a new model (N) or load old ones (O)")
            start_state = input()
            if start_state == "N" or start_state == "(N)":
                while True:
                    print("Define layers, excluding input and output layer. Example 16,16")
                    print("If you wish to use default input (X)")
                    layers = input()
                    if layers == "(X)" or layers == "X":
                        break
                    else:
                        for i, layer in enumerate(layers.split(",")):
                            layer = layer.strip()
                            if type(layer) == int:
                                inner_layers.append(layer.strip())
                            inner_layers = []
                            print(f"Layer {i + 1} is not int Layer {i} inputed value: {layer}")
                            break
                    if len(inner_layers) > 1:
                        break
                while True:
                    print("Define bias spread. Example 10 -> minumum bias: -10 maximum bias: 10")
                    print("If you wish to use default input (X)")
                    bias_spread = input()
                    if layers == "(X)" or layers == "X":
                        break
                    if type(bias_spread) == int:
                        break
                    print(f"Inputed bias spread is not a numberinputed value: {bias_spread}")
                print("Define name for the new model")
                print("If you wish to use default input (X)")
                name = input()
                if name == "(X)" or name == "X":
                    name = ""
                result = MS.create(name, inner_layers, bias_spread)
                if not result["status"]:
                    raise result["exception"]
                model = result["model"]
                break
            elif start_state == "O" or start_state == "(O)":
                path = ""
                while True:
                    print("Do you want load a single model (S) or multiple (M)")
                    load_state = input()
                    if load_state == "S" or load_state == "(S)":
                        print("Input model path")
                        path = input()
                        break
                    print(f"Not one of the options. Your answer: {start_state}, input S or M")
                model = FM.load()
                break
            else:
                print(f"Not one of the options. Your answer: {start_state}, input N or O")

        



        self.weights_vector = []
        self.weights_matrix = []
        self.biases_vector = []
        self.biases_matrix = []
        self.layer_sizes = []
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