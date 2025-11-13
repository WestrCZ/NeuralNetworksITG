import numpy as np
import random as rnd
import datetime
import json
from typing import Tuple

class ModelShaper():

    #Dimension definition - move elsewhere
    INPUT_SIZE = 784
    OUTPUT_SIZE = 10
    LAYER_SIZES = [INPUT_SIZE, 16, 16, OUTPUT_SIZE]
 
    def create_structure(dimensions, biases_lower_bound = -10, biases_upper_bound = 10, model_name = "") -> Tuple[bool, dict]: 
        dimensions[-1] = 10
        weights_length = 0
        biases_length = 0
        try:
            for i in range(len(dimensions) - 1):
                weights_length += dimensions[i] * dimensions[i + 1]
                biases_length += dimensions[i + 1]

            created_at = "".join(["-" if c == ":" else c for c in str(datetime.datetime.now())])
            model_name = "".join([c if (ord(c) > 96 and ord(c) < 123) or (ord(c) > 64 and ord(c) < 91) else "#" for c in str(model_name)])
            model_shape = {
                "model_name": model_name,
                "created_at": created_at,
                "dimensions": dimensions,
                "weights": [rnd.random() for _ in range(weights_length)],
                "biases": [rnd.randint(biases_lower_bound, biases_upper_bound) for _ in range(weights_length)]
            }
            with open(f"{model_name}_{created_at}.json", "w") as f:
                f.write(json.dumps(model_shape, indent=2),)
        except Exception as e:
            return False, {}, e
        return True, model_shape, None

    def to_matrices(model: dict) -> dict:
        dimensions = model["dimensions"]
        weights = model["weights"]
        biases = model["biases"]
        weights_array = np.empty(dimensions, dtype=np.ndarray)
        weights_index = 0

        for i in range(len(dimensions) - 1):
            weights_array[i] = np.empty(dimensions[i + 1], dtype=float)
            for _ in dimensions[i]:
                for j in range(dimensions[i + 1]):
                    weights_array[i][j] = weights[weights_index]
                    weights_index += 1 
            
    def to_vectors(weights: np.ndarray):
        print("bruh")

        