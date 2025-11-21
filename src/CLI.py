from infrastructure.model_shaper import ModelShaper as MS
from infrastructure.file_manager import FileManager as FM
from model import Model as Model
from pathlib import Path
from mnist import Mnist
import random as rnd
import numpy as np
import time
import ast

class CLI():
    def load() -> dict:
            result = {}
            while True:
                print("Please input whether you want to load a model (L) or load multiple (LM)")
                start = input().strip()
                if start == "(L)" or start == "L":
                    while True:
                        print("Input model path")
                        path = input().strip()
                        if Path(path).exists:
                            result = FM.load(path)
                            break
                        print(f"Not a valid path. inputed path: {path}")
                    if not result["status"]:
                        print(f"There was a problem with loading that model:\nException: {result["exception"]}")
                        return []
                    return [result["model"]]
                elif start == "(LM)" or start == "LM":
                    while True:
                        print("Input folder path")
                        path = input().strip()
                        if Path(path).exists:
                            result = FM.load_folder(path)
                            break
                        print(f"Not a valid path. inputed path: {path}")
                    if not result["status"]:
                        print(f"There was a problem with loading that folder not all models were loaded:\nException: {result["exception"]}")
                    return result["models"]
                print(f"Not one of the options. Your answer: {start}")

    def create() -> dict:
        result = {}
        inner_layers = []
        bias_spread = []
        while True:
            print("Do you wish to use default initialization? (Y/N)")
            default = input().strip()
            if default == "Y" or default == "(Y)":
                result = MS.create()
                if not result["status"]:
                    print(f"There was a problem with creating the default initialization:\nException: {result["exception"]}")
                    return []
                return [result["model"]]
            elif default == "N" or default == "(N)":
                while True:
                    print("Define layers, excluding input and output layer. Example 16,16")
                    print("If you wish to use default input (X)")
                    layers = input().strip()
                    if layers == "(X)" or layers == "X":
                        layers = [16, 16]
                        break
                    inner_layers = get_layer(layers, int)
                    if len(inner_layers) > 1:
                        break
                while True:
                    print("Define bias spread. Example: input is 10 -> minumum bias: -10 maximum bias: 10")
                    print("If you wish to use default input (X)")
                    bias_spread = input().strip()
                    if bias_spread == "(X)" or bias_spread == "X":
                        bias_spread = 10
                        break
                    if bias_spread.isdigit():
                        bias_spread = int(bias_spread)
                        break
                    print(f"Inputed bias spread is not a number. Inputed value: {bias_spread}")
                print("Define name for the new model")
                print("If you wish to use default input (X)")
                name = input().strip()
                result = MS.create("" if name == "(X)" or name == "X" else name, np.array(inner_layers), bias_spread)
                if not result["status"]:
                    print(f"There was a problem with creating the defined that model:\nException: {result["exception"]}")
                    return []
                return [result["model"]]
            print(f"Not one of the options. Your answer: {default}")

    def main():
        print("CLI app started") 
        print("Add models:")
        while True:
            models = {}
            while True:
                print("Do you want to create a model (R) or load models (L)")
                start = input()
                if start == "(R)" or start == "R":
                    models = [CLI.create()]
                elif start == "(L)" or start == "L":
                    models = CLI.load()
                else:
                    print(f"Not one of the options. Your answer: {start}")
                print("Do you wish to continue adding models (O) or end (E)")
                end = input()
                if end == "(O)" or end == "O":
                    continue
                elif end == "(E)" or end == "E":
                    break
                print(f"Not one of the options. Your answer: {end}")
            if models == []:
                print("No models added...")
                print("Ending program")
                return
            print("You can train or infer with models")
            while True:
                print("Do you want to infer with all (I) train all (T) or decide on each one (E)")
                all = input()
                if all == "(I)" or all == "I":
                    for model in models:
                        #add CLI input for forward pass
                        while True:
                            print(f"Input the the first layer. Match this length {model["dimensions"][0]}\n Example: 0.54, 0.9999, 0.31252")
                            print("If you wish to use random values (X)")
                            first_layer = input()
                            layer_list = []
                            if first_layer == "(X)" or first_layer == "X":
                                layer_list = [rnd.random() for _ in range(model["dimensions"][0])]
                                break
                            else:
                                layer_list = get_layer(first_layer, float)
                            if layer_list != []:
                                break
                        output = Model.forward(layer_list, model["weights"], model["biases"])
                        print(f"Model with name: {Model["name"]} output {output}")
                        #print and save all results
                        print("Not implemented yet")
                    break
                if all == "(T)" or all == "T":
                    data = Mnist.load_wrapped()
                    for model in models:
                        #training function here
                        #print and save all results
                        print("Not implemented yet")
                    break
                if all == "(E)" or all == "E":
                    for model in models:
                        while True:
                            print(f"Train (T) or Infer (I)\nModel name: {model["name"]}")
                            each = input()
                            data = Mnist.load_wrapped()
                            if each == "(T)" or each == "T":
                                #training function here
                                #print and save results
                                print("Not implemented yet")
                                break
                            elif each == "(I)" or each == "I":
                                #add CLI input for forward pass
                                while True:
                                #MR.forward_pass()
                                #print and save results
                                print("Not implemented yet")
                                break
                            print(f"Not one of the options. Your answer: {each}")
                    break
            print("Run program again? (Y/N)")
            again = input()
            if again == "(N)" or again == "N":
                break
        print("All models adressed\nEnding program ...")
        time.sleep(2)

def get_layer(layer: str, element_type: type) -> list:
    layer_list = []
    for i, x in enumerate(layer.split(",")):
        x = x.strip()
        x_type = ast.literal_eval(layer)
        if x != element_type:
            print(f"Layer {i + 1} is not {element_type}. Layer {i + 1} inputed value: {layer} with type {x_type}")
            layer_list = []
            break
        layer_list.append(element_type(layer))
    return layer_list

if __name__ == "__main__":
    CLI.main()