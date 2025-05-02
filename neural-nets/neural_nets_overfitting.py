import tensorflow as tf
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfTransformer
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

print("\nSTART\n")

# Read in data
df = pd.read_csv("../text-mining-project-data/clean/count-4856.csv")
labels = df.pop("labels")

# Encode labels
enc = LabelEncoder()
enc_labels = enc.fit_transform(labels)

# Neural Net with count data
x_train, x_test, y_train, y_test = train_test_split(df, enc_labels, train_size=0.85)

# Build model
model = tf.keras.models.Sequential([
    tf.keras.layers.Dense(128, activation='relu'),
    tf.keras.layers.Dropout(0.2),
    tf.keras.layers.Dense(1)
])

model.compile(optimizer='adam',
              loss=tf.keras.losses.binary_crossentropy,
              metrics=['accuracy'])

# Testing multiple epochs
n_epochs = np.arange(1, 6)
training_loss = np.zeros(n_epochs.shape[0])
testing_loss = np.zeros(n_epochs.shape[0])
training_accs = np.zeros(n_epochs.shape[0])
testing_accs = np.zeros(n_epochs.shape[0])

for i, n_ep in enumerate(n_epochs):
    model.fit(np.array(x_train), np.array(y_train), epochs=n_ep, batch_size=32)
    training_loss[i], training_accs[i] = model.evaluate(x_train, y_train)
    testing_loss[i], testing_accs[i] = model.evaluate(x_test, y_test)

above_5p_idx = np.where(training_accs >= 0.05 + testing_accs)[0][0]
above_5p = n_epochs[above_5p_idx]

plt.title("Training vs Testing Accuracies for Feed Forward Neural Network\nCount Data")
plt.xlabel("Epochs")
plt.ylabel("Accuracy")
plt.plot(n_epochs, training_accs, label="training data")
plt.plot(n_epochs, testing_accs, label="testing data")
plt.axvline(x=above_5p, label=">= 5% Difference", color="red", linestyle="--")
plt.legend()
plt.savefig("accs-plot-count.png")
plt.clf()

# Test with the tfidf data frame
tfidf_trans = TfidfTransformer()
tfidf_df = tfidf_trans.fit_transform(df).toarray()

x_train, x_test, y_train, y_test = train_test_split(tfidf_df, enc_labels, train_size=0.85)
for i, n_ep in enumerate(n_epochs):
    model.fit(np.array(x_train), np.array(y_train), epochs=n_ep, batch_size=32)
    training_loss[i], training_accs[i] = model.evaluate(x_train, y_train)
    testing_loss[i], testing_accs[i] = model.evaluate(x_test, y_test)

above_5p_idx = np.where(training_accs >= 0.05 + testing_accs)[0][0]
above_5p = n_epochs[above_5p_idx]
plt.title("Training vs Testing Accuracies for Feed Forward Neural Network\nTFIDF Data")
plt.xlabel("Epochs")
plt.ylabel("Accuracy")
plt.plot(n_epochs, training_accs, label="training data")
plt.plot(n_epochs, testing_accs, label="testing data")
plt.axvline(x=above_5p, label=">= 5% Difference", color="red", linestyle="--")
plt.legend()
plt.savefig("accs-plot-tfidf.png")
