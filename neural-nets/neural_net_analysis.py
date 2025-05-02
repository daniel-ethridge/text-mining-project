import tensorflow as tf
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
from sklearn.metrics import f1_score
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import dataframe_image as dfi

# Read in data
df = pd.read_csv("../text-mining-project-data/clean/count-4856.csv")
labels = df.pop("labels")

# Encode labels
enc = LabelEncoder()
enc_labels = enc.fit_transform(labels)
print(enc.transform(["right", "left"]))

# Convert to tfidf
df_tfidf = TfidfTransformer().fit_transform(df).toarray()

# create train_test_split
x_train, x_test, y_train, y_test = train_test_split(df_tfidf, enc_labels)

# Build model
model = tf.keras.models.Sequential([
    tf.keras.layers.Dense(128, activation='relu'),
    tf.keras.layers.Dropout(0.2),
    tf.keras.layers.Dense(1)
])

# Compile model
model.compile(optimizer='adam',
              loss=tf.keras.losses.binary_crossentropy,
              metrics=['accuracy', 'precision', 'recall'])

# Fit model
model.fit(np.array(x_train), np.array(y_train), epochs=2, batch_size=32)

# Calculate metrics
loss, acc, prec, rec = model.evaluate(x_test, y_test)
y_pred_probs = model.predict(x_test)
y_pred = (y_pred_probs > 0.5).astype("int32").flatten()
f1 = f1_score(y_test, y_pred)
conf_mat = confusion_matrix(y_test, y_pred)

metrics = {
    "accuracy": acc,
    "precision": prec,
    "recall": rec,
    "f1 score": f1
}

mets_df = pd.DataFrame(metrics, index=["Neural Network"])
mets_df.to_csv("mets_df.csv")

# Create confusion matrix
mat_display = ConfusionMatrixDisplay(conf_mat, display_labels=["left", "right"]).plot()
mat_display.ax_.set_title("Confusion Matrix for Neural Network")
plt.savefig("conf-mat.png")
