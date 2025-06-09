from mnist_preprocess import load_preprocessed_data

train, val, test = load_preprocessed_data()

print(f"Train data size: {len(train)}")
print(f"Validation data size: {len(val)}")
print(f"Test data size: {len(test)}")

print(f"First training input shape: {train[0][0].shape}")
print(f"First training label shape: {train[0][1].shape}")
print(f"First training label vector (one-hot):\n{train[0][1]}")

print(f"First validation label: {val[0][1]}")
print(f"First test label: {test[0][1]}")
