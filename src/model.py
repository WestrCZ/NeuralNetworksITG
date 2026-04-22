from Utils.operations import Operations, ACTIVATION_FUNCTIONS
from datetime import datetime as Date
from typing import List
from copy import deepcopy
import hashlib
import orjson
import random as rnd
import math
import os

#TODO add important parameters/constants to global config

MODEL_FOLDER_PATH = os.path.join(os.path.dirname(__file__), "..\\models")

class Model():    
    def __init__(self, dimensions: List[int], activation: str, epochs: int, batch_size: int, learning_rate: float):
        try:
            found = False
            for a in ACTIVATION_FUNCTIONS:
                if a == activation:
                    found = True
                    break
            if found == False:
                error_message = f"Inputed activation is not supported. Inputed epochs: {activation}\nSupported activations are:"
                for a in ACTIVATION_FUNCTIONS:
                    error_message += f" {a}"
                raise Exception(error_message) 
            if type(epochs) != int:
                raise Exception(f"Epochs must be an int. Inputed epochs: {epochs}, Type: {type(epochs)}") 
            elif epochs < 1:
                raise Exception(f"Epochs must be larger than 0. Inputed epochs: {epochs}") 
            if type(batch_size) != int:
                raise Exception(f"Batch size must be an int. Inputed batch_size: {batch_size}, Type: {type(batch_size)}")
            elif batch_size < 1:
                raise Exception(f"Batch size must be larger than 0. Inputed batch_size: {batch_size}")
            if type(learning_rate) != float:
                raise Exception(f"Leaning rate  must be either a float or an int. Inputed learning_rate: {learning_rate}, Type: {type(batch_size)}")
            elif learning_rate < 0:
                raise Exception(f"Learning rate must be larger than 0. Inputed learning_rate: {batch_size}")
            
            time_now = Date.now().__str__()
            self.id = hashlib.md5(f"{"ITG"}+{time_now}".encode()).hexdigest()
            self.created_at = time_now     
            self.path = None  
            self.dimensions = dimensions
            self.activation = activation
            self.epochs = epochs
            self.batch_size = batch_size
            self.learning_rate = learning_rate
            self.biases = None
            self.weights = None
        except Exception as e:
            raise Exception(f"An exception occured while creating a model: Exception: {e}")
    
    def train(self, x: List[List[float]], y: List[List[int]]):
        try:
            if len(x) != len(y):
                raise Exception(f"Inputed X\'s ans Y\'s have mismatching lengths. Length of X\'s: {len(x)} Length of Y\'s: {len(x)}")
            rnd.seed("0")
            self.biases = []
            self.weights = []
            #inializing parameters
            for i in range(1, len(self.dimensions)):
                self.biases.append([])
                self.weights.append([])    
                #xavier initialization        
                limit = math.sqrt(6 / (self.dimensions[i - 1] + self.dimensions[i]))   
                for j in range(self.dimensions[i - 1]):                                     
                    self.weights[i - 1].append([])
                    for _ in range(self.dimensions[i]):                                       
                        self.weights[i - 1][j].append(rnd.uniform(-limit, limit))
                for j in range(self.dimensions[i]):
                    self.biases[i - 1].append(rnd.uniform(-limit, limit))   
            #making batches for training
            batch_count = math.ceil(len(x) / self.batch_size) 
            if batch_count == 0:
                batch_count = 1
            batches = []
            for i in range(batch_count):
                slice_start = i * self.batch_size
                slice_end = (i + 1) * self.batch_size
                if slice_end > len(x):
                    slice_end = len(x)
                batch = []
                for j in range(slice_start, slice_end):
                    batch.append((x[j], y[j]))
                batches.append(batch)  
            #training
            for epoch in range(self.epochs):                       
                loss_avg = 0.0   
                for i, batch in enumerate(batches):                 
                    for j, datum in enumerate(batch): 
                        activations = self.__forward(datum[0])  
                        answer = max(datum[1])
                        self.__backward(activations, datum[1].index(answer))             
                        loss_avg += Operations.cross_entropy(activations[-1], datum[1].index(answer))
                print(f"Epoch: {epoch + 1}\nAverage loss: {loss_avg / len(x)}")
        except Exception as e:
            raise Exception(f"An exception occured while a training a model: Model id: {self.id}. Exception: {e}")
        
    def classify(self, activations: List[float], layer_index: int = 0) -> List[float]:
        """
        Function for classification
        activations is th input layer
        Always call without setting layer_index, this is a recursive function
        """
        try:
            if len(activations) != self.dimensions[layer_index]:
                raise Exception(f"Input has mismatching length. Length of input: {len(activations)}. Size of dimension {layer_index}: {self.dimensions[layer_index]}")
            zeds = Operations.vector_addition(Operations.vector_matrix_product(activations, self.weights[layer_index]), self.biases[layer_index])
            if layer_index < len(self.weights) - 1:
                layer_index += 1
                return self.classify([Operations.get_activation(x, self.activation) for x in zeds], layer_index)
            else:
                return Operations.softmax(zeds)
        except Exception as e:
            Exception(f"An exception occured while a model was classifying: Model id: {self.id}. Input: {activations}. Exception: {e}")      

    #infrastructure

    def __forward(self, input) -> List[List[float]]:
        #getting activations by passing forward
        activations = []
        activations.append(input) 
        for l in range(len(self.weights)):
            zeds = Operations.vector_addition(
                Operations.vector_matrix_product(
                    activations[l], 
                    self.weights[l]), 
                self.biases[l]
            )
            if l < len(self.weights) - 1:
                activations.append([Operations.get_activation(x, self.activation) for x in zeds])
            else:
                activations.append(Operations.softmax(zeds))
        return activations
    
    def __backward(self, activations: List[List[float]], answer_index: List[int]):
        #backpropagation - gradient descent
        delta = deepcopy(activations[-1])
        delta[answer_index] -= 1
        for l in range(1, len(self.weights)):  
            for i in range(len(self.biases[-l])):
                self.biases[-l][i] -= delta[i] * self.learning_rate
            for i, delta_element in enumerate(delta):
                for j, activation in enumerate(activations[-(l + 1)]):
                    self.weights[-l][j][i] -= delta_element * activation * self.learning_rate
            if l + 1 < len(self.weights):
                delta = Operations.vector_matrix_product(delta, self.weights[-l], True)
                delta = [
                    delta[i] 
                    * Operations.get_activation_derivative(activation, self.activation)
                    for i, activation in enumerate(activations[-(l + 1)])
                ]

    def measure_accuracy(self, x: List[List[float]], y: List[List[int]]) -> float:
        try:
            if len(x) != len(y):
                raise Exception(f"Inputed X\'s ans Y\'s have mismatching lengths. Length of X\'s: {len(x)}. Length of Y\'s: {len(x)}")
            success = 0
            for i in range(len(x)):
                classification = self.classify(x[i])
                if classification.index(max(classification)) == y[i].index(max(y[i])):
                    success += 1
            return success / len(x)
        except Exception as e:
            Exception(f"An exception occured while measuring accuracy of a model: Model id: {self.id}. Exception: {e}")

    def save(self):
        try:
            path = os.path.join(MODEL_FOLDER_PATH, f"Model_{self.id[:10]}.json")
            if os.path.exists(path) == True:
                path = os.path.join(MODEL_FOLDER_PATH, f"Model{self.id}.json")
            if os.path.exists(path) == True:
                raise Exception(f"The path already exists")
            self.path = path
            os.makedirs(os.path.dirname(self.path))
            with open(self.path, "w") as f:
                f.write(orjson.dumps(
                    self.__dict__, 
                    option=orjson.OPT_INDENT_2).decode()
                )
        except Exception as e:
            raise Exception(f"An exception occured while saving the model to path: Model id: {self.id}. Path: {path}. Exception: {e}")
    
    def load(self, path: str):
        try:
            model_dict = dict(orjson.loads(open(path).read()))
            self.__dict__ = model_dict
        except Exception as e:
            raise Exception(f"An exception occured while loading a model from path: Model id: {self.id}. Path: {path}. Exception: {e}")
    