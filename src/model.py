from infrastructure.model_shaper import ModelShaper as MO
import numpy as np

class Model:
    def forward(activations: np.ndarray, weights: np.ndarray, biases: np.ndarray, layer_index = 0) -> np.ndarray:
        """
        Forward pass
        Function for inference
        Always call without setting layer_index - recursive function
        The model has to be formatted to matrices using the ModelShaper.to_matrices() function
        Activations is the input layer
        """
        activations = np.array
        (
            [
                MO.sigmoid(x) for x in MO.vector_addition(MO.matrix_x_vector(weights[layer_index], activations), biases[layer_index])
            ]
        )
        layer_index += 1
        if layer_index < len(weights):
            return Model.forward(activations, weights, biases, layer_index)
        else:
            return activations
#TODO Think about just inputing np.empty(len(weights)) into layers_activations instead of the odious new if
    def forward_train(activations: np.ndarray, weights: np.ndarray, biases: np.ndarray, layers_activations: np.ndarray, layer_index = 0) -> np.ndarray:
        """
        Forward pass
        Function for training
        Always call without setting layer_index - recursive function
        The model has to be formatted to matrices using the ModelShaper.to_matrices() function
        Activations is the input layer
        """
        layers_activations = np.empty(len(weights)) if layer_index == 0 else layers_activations #TODO think of a better name for layers_activations
        layers_activations[layer_index] = np.array
        (
            [
                MO.sigmoid(x) for x in MO.vector_addition(MO.matrix_x_vector(weights[layer_index], activations), biases[layer_index])
            ]
        )
        layer_index += 1
        if layer_index < len(weights):
            return Model.forward(layers_activations[layer_index], weights, biases, layers_activations, layer_index)
        else:
            return layers_activations