from pathlib import Path as Path
import numpy as np
import json
import os

class FileManager():
    def save(model: dict) -> dict:
        try:
            name = "".join([c if (ord(c) > 96 and ord(c) < 123) or (ord(c) > 64 and ord(c) < 91) else "#" for c in str(model["name"])]) #c stands for char
            folder_path = Path(f"{Path().resolve()}/models")
            if not folder_path.is_dir():
                os.mkdir(folder_path)
            path = f"{folder_path}\\{name}_{model["created_at"]}.json"
            model["name"] = name    
            model["biases"] = list(model["biases"])
            model["weights"] = list(model["weights"])
            model["path"] = path
            with open(path, "w") as f:
                f.write(json.dumps(model, indent=2))
            model["biases"] = np.array(model["biases"])
            model["weights"] = np.array(model["weights"])
            exception = None
        except Exception as e:
            exception = e
        return {
            "status": True if exception is None else False,
            "model": model if exception is None else {},
            "exception": exception
        }
    
    def load(path: str) -> dict:
        try:
            model = json.load(open(path, "r"))
            model["biases"] = np.array(model["biases"])
            model["weights"] = np.array(model["weights"])
            exception = None
        except Exception as e:
            exception = e
        return {
            "status": True if exception is None else False,
            "model": model if exception is None else {},
            "exception": exception
        }
    def load_folder(folder_path: str) -> dict:
        models = [] 
        try:
            for path in Path(folder_path).iterdir():
                result = FileManager.load(path)
                if result["status"]:
                    models.append(result["model"])
                else:
                    raise Exception(result["exception"])
            exception = None
        except Exception as e:
            exception = e
        return {
            "status": True if exception is None else False,
            "models": models if exception is None else [],
            "exception": exception
        }
    def save_results(resutls: np.array) -> dict:
        #implement sessions which will record the result of a forward pass, what model was used using id and name
        #add ids to model .jsons
        print("Not implemented")