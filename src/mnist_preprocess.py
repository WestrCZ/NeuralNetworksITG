import os
import numpy as np  # type: ignore
from mnist_loader import load_data_wrapper

def save_preprocessed_data(filepath='./data/mnist_preprocessed.npz'):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)

    training_data, validation_data, test_data = load_data_wrapper()
    
    train_x = np.array([x.flatten() for x, y in training_data])
    train_y = np.array([y.flatten() for x, y in training_data])
    val_x = np.array([x.flatten() for x, y in validation_data])
    val_y = np.array([y for x, y in validation_data])
    test_x = np.array([x.flatten() for x, y in test_data])
    test_y = np.array([y for x, y in test_data])
    
    np.savez_compressed(filepath,
                        train_x=train_x, train_y=train_y,
                        val_x=val_x, val_y=val_y,
                        test_x=test_x, test_y=test_y)
    print(f"Data saved to {filepath}")

def load_preprocessed_data(filepath='./data/mnist_preprocessed.npz'):
    data = np.load(filepath)
    training_data = list(zip(
        [x.reshape((784,1)) for x in data['train_x']],
        [y.reshape((10,1)) for y in data['train_y']]
    ))
    validation_data = list(zip(
        [x.reshape((784,1)) for x in data['val_x']],
        data['val_y']
    ))
    test_data = list(zip(
        [x.reshape((784,1)) for x in data['test_x']],
        data['test_y']
    ))
    return training_data, validation_data, test_data

if __name__ == '__main__':
    save_preprocessed_data()
