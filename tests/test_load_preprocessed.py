from mnist_preprocess import load_preprocessed_data
import matplotlib.pyplot as plt

train, val, test = load_preprocessed_data()

example_train = train[201] # You can choose any (in range ofc)
example_val = val[0]
example_test = test[0]

print(f"Train data size: {len(train)}")
print(f"Validation data size: {len(val)}")
print(f"Test data size: {len(test)}")

print(f"First training input shape: {example_test[0].shape}")
print(f"First training label shape: {example_test[1].shape}")
print(f"First training label vector (one-hot):\n{example_test[1]}")

print(f"First validation label: {example_val[1]}")
print(f"First test label: {example_train[1]}")
print(f"Vstupní data: {example_train[0]}")

# Visualization

train_img = example_train[0].reshape(28,28)
val_img = example_val[0].reshape(28,28)
test_img = example_test[0].reshape(28,28)

plt.figure(figsize=(10, 5))

plt.subplot(1, 3, 1)
plt.imshow(train_img, cmap='gray')
plt.title(f"Label: Train")
plt.axis('off')

plt.subplot(1, 3, 2)
plt.imshow(val_img, cmap='gray')
plt.title(f"Label: Validation")
plt.axis('off')

plt.subplot(1, 3, 3)
plt.imshow(test_img, cmap='gray')
plt.title(f"Label: Test")
plt.axis('off')

plt.tight_layout()
plt.show()