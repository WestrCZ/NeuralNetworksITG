from infrastructure.model_shaper import ModelShaper as MS
from infrastructure.file_manager import FileManager as FM
from pathlib import Path as Path
import time

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
                    else:
                        for i, layer in enumerate(layers.split(",")):
                            layer = layer.strip()
                            if not layer.isdigit():
                                inner_layers = []
                                print(f"Layer {i + 1} is not int. Layer {i + 1} inputed value: {layer}")
                                break
                            inner_layers.append(int(layer.strip()))
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
                result = MS.create("" if name == "(X)" or name == "X" else name, inner_layers, bias_spread)
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
                print("Do you want to infer will all (I) train all (T) or decide on each one (E)")
                all = input()
                if all == "(I)" or all == "I":
                    for model in models:
                        #add input for forward pass GUI or CLI
                        #MR.forward_pass()
                        #print and save all results
                        print("Not implemented yet")
                    break
                if all == "(T)" or all == "T":
                    for model in models:
                        #input from mnist db
                        #training function here
                        #print and save all results
                        print("Not implemented yet")
                    break
                if all == "(E)" or all == "E":
                    for model in models:
                        while True:
                            print(f"Train (T) or Infer (I)\nModel name: {model["name"]}")
                            each = input()
                            if each == "(T)" or each == "T":
                                #input from mnist db
                                load_data_wrapper()#unfinished call
                                #training function here
                                #print and save results
                                print("Not implemented yet")
                                break
                            elif each == "(I)" or each == "I":
                                #add input for forward pass
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
if __name__ == "__main__":
    CLI.main()