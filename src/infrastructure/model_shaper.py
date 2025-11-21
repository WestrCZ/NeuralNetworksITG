from infrastructure.file_manager import FileManager as FM
from datetime import datetime as Date
import random as rnd
import numpy as np

class ModelShaper():
    def create(name = "", dimensions = [16, 16], bias_spread = 10) -> dict: 
        """
        dimensions are just inner layers of the neural network
        """
        dimensions.append(10)
        dimensions.insert(0, 784)
        weights = []
        biases = []
        for i in range(1, len(dimensions)):
            weights += [rnd.random() for _ in range(dimensions[i] * dimensions[i - 1])]
            biases += [rnd.randint(-bias_spread, bias_spread) for _ in range(dimensions[i])]
        model = {
            "name": name,
            "created_at": "".join(["-" if c == ":" else c for c in str(Date.now())]), #c stands for char
            "path": "",
            "dimensions": dimensions,
            "biases": biases,
            "weights": weights
        }
        return FM.save(model)
    
    def to_matrices(model: dict) -> dict:
        dimensions = model["dimensions"]
        biases = np.empty(len(dimensions) - 1, dtype=np.ndarray)
        weights = np.empty(len(dimensions) - 1, dtype=np.ndarray)
        biases_index = 0
        weights_index = 0
        for i in range(1, len(dimensions)):
            biases[i - 1] = model["biases"][biases_index : biases_index + dimensions[i]]
            weights[i - 1] = np.empty((dimensions[i], dimensions[i - 1]))
            for j in range(1, dimensions[i]):
                for k in range(1, dimensions[i - 1]):
                    weights[i - 1][j][k] = model["weights"][weights_index]
                    weights_index += 1
            biases_index += dimensions[i]
        model["biases"] = biases
        model["weights"] = weights
        return model
            
    def to_vectors(model: dict) -> dict:
        biases = []
        weights = []
        for i in range(1, len(model["dimensions"])):
            for j in range(len(model["weights"][i - 1])):
                for k in range(len(model["weights"][i - 1][j])):
                    weights.append(model["weights"][i - 1][j][k])
            biases += list(model["biases"][i - 1])

        model["biases"] = np.array(biases)
        model["weights"] = np.array(weights)
        return model