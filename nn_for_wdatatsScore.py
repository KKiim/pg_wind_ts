import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras.callbacks import EarlyStopping
import matplotlib.pyplot as plt
import numpy as np

# Load the data
file_path = 'heightGainData_with_hm_scores.csv'
data = pd.read_csv(file_path)

# Select the relevant columns
X = data[['Wind Speed Avg (km/h)', 'Wind Speed Min (km/h)', 'Wind Speed Max (km/h)']]
y = data['Score']

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Standardize the features
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# Build the neural network model
model = Sequential([
    Dense(64, activation='relu', input_shape=(X_train.shape[1],)),
    Dropout(0.3),  # Adding dropout for regularization
    Dense(1)
])

# Compile the model
model.compile(optimizer='adam', loss='mse', metrics=['mae'])

# Define early stopping callback
early_stopping = EarlyStopping(monitor='val_loss', patience=10, restore_best_weights=True)

# Train the model
history = model.fit(X_train, y_train, epochs=100, batch_size=32, validation_split=0.2, verbose=1, callbacks=[early_stopping])

# Evaluate the model
test_loss, test_mae = model.evaluate(X_test, y_test, verbose=1)
print(f'Test MAE: {test_mae}')

# Predict the scores
y_pred = model.predict(X_test)

# Display the results
results = pd.DataFrame({'Actual': y_test, 'Predicted': y_pred.flatten()})
print(results.head())

# Plot training & validation loss values
plt.figure(figsize=(10, 6))
plt.plot(history.history['loss'], label='Train Loss')
plt.plot(history.history['val_loss'], label='Validation Loss')
plt.title('Model Loss')
plt.xlabel('Epoch')
plt.ylabel('Loss')
plt.legend(loc='upper right')
plt.show()

# Plot training & validation MAE values
plt.figure(figsize=(10, 6))
plt.plot(history.history['mae'], label='Train MAE')
plt.plot(history.history['val_mae'], label='Validation MAE')
plt.title('Model MAE')
plt.xlabel('Epoch')
plt.ylabel('MAE')
plt.legend(loc='upper right')
plt.show()

# Test with new test values
test_values = np.array([
    [15.0, 0.0, 25.0],
    [16.0, 1.0, 26.0],
    [17.0, 2.0, 27.0],
    [18.0, 3.0, 28.0],
    [19.0, 4.0, 29.0],
    [20.0, 5.0, 30.0],
    [21.0, 6.0, 31.0],
    [22.0, 7.0, 32.0],
    [23.0, 8.0, 33.0],
    [24.0, 9.0, 34.0],
    [25.0, 10.0, 35.0],
    [16.0, 11.0, 26.0],
    [17.0, 12.0, 27.0],
    [18.0, 13.0, 28.0],
    [19.0, 14.0, 29.0],
    [20.0, 15.0, 30.0],
    [21.0, 0.0, 31.0],
    [22.0, 1.0, 32.0],
    [23.0, 2.0, 33.0],
    [24.0, 3.0, 34.0],
    [25.0, 4.0, 35.0],
    [16.0, 5.0, 26.0],
    [17.0, 6.0, 27.0],
    [18.0, 7.0, 28.0],
    [19.0, 8.0, 29.0]
])

# Standardize the test values using the same scaler
test_values_scaled = scaler.transform(test_values)

# Predict the scores using the trained model
predicted_scores = model.predict(test_values_scaled)

# Print the input values and the predicted scores
for i, (input_val, pred) in enumerate(zip(test_values, predicted_scores)):
    print(f'Input Values {i+1}: {input_val}, Predicted Score: {pred[0]}')
