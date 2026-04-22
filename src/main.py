from trainer import Trainer
from model import Model
import orjson
import gzip
import os

#TODO add filepath to global config
DATA_PATH = os.path.join("data", "mnist_preprocessed_vector.gz")

if __name__ == "__main__":
    path = "c:/Users/matej/source/MLITG/data/mnist_preprocessed_vector.gz"
    data = orjson.loads(gzip.open(path).read())
    trainer = Trainer(
        max_depth=3, 
        layer_size_start=256, 
        layer_size_end=300, 
        epochs_start=3, 
        epochs_end=3, 
        batch_size_start=1000, 
        batch_size_end=2000,
        learning_rate_start=0.005,
        learning_rate_end=0.02,
        activation="relu"
    )
    model = trainer.random_search(data["training_x"], data["training_y"], data["validation_x"], data["validation_y"])
    #model = Model([len(data["training_x"][0]), 256, len(data["training_y"][0])], "relu", 3, 1000, 0.01)
    #model.train(data["training_x"], data["training_y"])
    print(model.measure_accuracy(data["testing_x"], data["testing_y"]))
