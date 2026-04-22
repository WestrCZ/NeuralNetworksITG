from Utils.operations import Operations, ACTIVATION_FUNCTIONS
from model import Model
from copy import deepcopy
from typing import List
import random as rnd

#TODO exception raising and management

class Trainer():
    def __init__(self, max_depth: int, layer_size_start: int, layer_size_end: int,
        epochs_start: int, epochs_end: int, batch_size_start: int, batch_size_end: int, 
        learning_rate_start: float, learning_rate_end: int, activation: str = None):
        try:
            self.keys = ["epochs", "batch_size", "learning_rate", "activation"]
            self.start = {
                    "max_depth": 2,
                    "epochs": epochs_start,
                    "batch_size": batch_size_start,
                    "learning_rate": learning_rate_start,
                    "activation": 0 if activation == None else ACTIVATION_FUNCTIONS.index(activation)
                }
            self.end = {
                    "max_depth": max_depth,
                    "epochs": epochs_end,
                    "batch_size": batch_size_end,
                    "learning_rate": learning_rate_end,
                    "activation": len(ACTIVATION_FUNCTIONS) - 1 if activation == None else ACTIVATION_FUNCTIONS.index(activation)
                }
            self.step={}
            for i in range(max_depth - 2):
                self.keys.append(str(i))
                self.start[str(i)] = layer_size_start
                self.end[str(i)] = layer_size_end
        except Exception as e:
            Exception(f"An exception occured while creating a Trainer: Exception: {e}")

    def grid_search(self, train_x: List[List[float]], train_y: List[List[float]], validation_x: List[List[float]], validation_y: List[List[float]], 
        layer_size_step: int = 10, epochs_step: int = 1, batch_size_step: int = 100, learning_rate_step: float = 0.001) -> Model:
        self.step = {
            "epochs": epochs_step,
            "batch_size": batch_size_step,
            "learning_rate": learning_rate_step,
            "activation": 1
        }
        start_layers = None
        if self.end["max_depth"] - 2 > 0:
            start_layers = []
            for i in range(self.end["max_depth"] - 2):
                self.step[str(i)] = layer_size_step
                start_layers.append(self.start[str(i)])
                
        #dimensions = [] if start_layers == None else start_layers
        #dimensions.insert(0, len(train_x[0])) #input dimension size
        #dimensions.append(len(train_y[0])) #output dimension size
        #best_model = Model(
        #    dimensions, 
        #    ACTIVATION_FUNCTIONS[self.start["activation"]], 
        #    self.start["epochs"], 
        #    self.start["batch_size"], 
        #    self.start["learning_rate"]
        #) 
        #best_accuracy = best_model.measure_accuracy(validation_x, validation_y)
        best_model = None
        best_accuracy = -1.0
        for i in range(len(self.keys) - 1, -1, -1):
            for j in range(len(self.keys) - i):
                key_combination = self.keys[:i]
                key_combination.append(self.keys[i + j])
                varied_values = deepcopy(self.start)
                dimensions = []
                if start_layers != None:
                    dimensions = [] if Operations.try_parse(key_combination[-1]) == None else start_layers[:(int(key_combination[-1]) + 1)]
                    dimensions.insert(0, len(train_x[0])) #input dimension size
                    dimensions.append(len(train_y[0])) #output dimension size
                if j == 1: 
                    best_model = Model(
                        dimensions, 
                        ACTIVATION_FUNCTIONS[self.start["activation"]], 
                        self.start["epochs"], 
                        self.start["batch_size"], 
                        self.start["learning_rate"]
                    )
                    best_model.train(train_x, train_y) 
                    accuracy = model.measure_accuracy(validation_x, validation_y) 
                while (True):
                    changes = False 
                    for key in key_combination:
                        varied_values[key] = varied_values[key] + self.step[key]
                        if varied_values[key] > self.end[key]:
                            varied_values[key] = self.end[key] 
                        else:
                            if Operations.try_parse(key) != None:
                                dimensions[int(key)] = varied_values[key]
                            changes = True 
                    if changes == False:
                        break               
                    model = Model(
                        dimensions, 
                        ACTIVATION_FUNCTIONS[varied_values["activation"]], 
                        varied_values["epochs"], 
                        varied_values["batch_size"], 
                        varied_values["learning_rate"]
                    )
                    model.train(train_x, train_y) 
                    accuracy = model.measure_accuracy(validation_x, validation_y)
                    if accuracy > best_accuracy:
                        best_accuracy = accuracy
                        best_model = deepcopy(model)
                    print(f"Achieved accuracy {accuracy} with config: {varied_values}")
        return best_model
    
    def random_search(self, train_x: List[List[float]], train_y: List[List[float]], validation_x: List[List[float]], validation_y: List[List[float]], iterations: int = 10) -> Model:
        rnd.seed("1")
        best_accuracy = -1.0
        best_model = None 
        for _ in range(iterations):
            dimensions = []
            for key in self.keys:
                if key == "learning_rate":
                    self.step[key] = rnd.uniform(self.start[key], self.end[key])
                else:
                    self.step[key] = rnd.randint(self.start[key], self.end[key])
                    if Operations.try_parse(key) != None:
                        dimensions.append(self.step[key])
            dimensions.insert(0, len(train_x[0])) #input dimension size
            dimensions.append(len(train_y[0])) #output dimension size
            model = Model(
                dimensions, 
                ACTIVATION_FUNCTIONS[self.step["activation"]], 
                self.step["epochs"], 
                self.step["batch_size"], 
                self.step["learning_rate"]
            )
            model.train(train_x, train_y) 
            accuracy = model.measure_accuracy(validation_x, validation_y)
            if accuracy > best_accuracy:    
                best_accuracy = accuracy
                best_model = deepcopy(model)
            print(f"Achieved accuracy {accuracy} with config: {self.step}")
        return best_model
