from mnist_preprocess import load_preprocessed_data
import matplotlib.pyplot as plt

train, val, test = load_preprocessed_data()

print(f"Train data size: {len(train)}")
print(f"Validation data size: {len(val)}")
print(f"Test data size: {len(test)}")

print(f"First training input shape: {train[0][0].shape}")
print(f"First training label shape: {train[0][1].shape}")
print(f"First training label vector (one-hot):\n{train[0][1]}")

print(f"First validation label: {val[0][1]}")
print(f"First test label: {test[0][1]}")
print(f"Vstupní data: {train[0][0]}")

# Visualization
X_train = train[201][0].reshape(28, 28) 
X_val = val[0][0].reshape(28,28)
X_test = test[0][0].reshape(28,28)

plt.figure(figsize=(10, 5))

plt.subplot(1, 3, 1)
plt.imshow(X_train, cmap='gray')
plt.title(f"Label: Train")
plt.axis('off')

plt.subplot(1, 3, 2)
plt.imshow(X_val, cmap='gray')
plt.title(f"Label: Validation")
plt.axis('off')

plt.subplot(1, 3, 3)
plt.imshow(X_test, cmap='gray')
plt.title(f"Label: Test")
plt.axis('off')

plt.tight_layout()
plt.show()