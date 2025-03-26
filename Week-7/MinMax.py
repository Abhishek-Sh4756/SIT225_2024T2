import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt


df = pd.read_csv('Task_7.csv')  # Assuming columns: Temperature, Humidity

# 2. Prepare data
X = df[['Temperature']].values
y = df['Humidity'].values

# 3. Train the model
model = LinearRegression()
model.fit(X, y)

# 4. Find min/max temperatures
min_temp = np.min(X)
max_temp = np.max(X)
print(f"Minimum temperature: {min_temp:.2f}°C")
print(f"Maximum temperature: {max_temp:.2f}°C")

# 5. Create 100 test temperature values
test_temps = np.linspace(min_temp, max_temp, 100).reshape(-1, 1)

# 6. Predict humidity for all test values
predicted_humidity = model.predict(test_temps)

# 7. Create DataFrame with predictions
results = pd.DataFrame({
    'Test_Temperature': test_temps.flatten(),
    'Predicted_Humidity': predicted_humidity
})

# 8. Save predictions to CSV
results.to_csv('temperature_humidity_predictions.csv', index=False)
print("Predictions saved to 'temperature_humidity_predictions.csv'")

# 9. Visualize
plt.figure(figsize=(12, 6))
plt.scatter(X, y, color='blue', alpha=0.5, label='Actual Data')
plt.plot(test_temps, predicted_humidity, color='red', linewidth=2, label='Regression Line')
plt.scatter(test_temps, predicted_humidity, color='green', s=10, alpha=0.7, label='Test Predictions')

plt.title('Temperature vs Humidity: Predictions Across Range', fontsize=14)
plt.xlabel('Temperature (°C)', fontsize=12)
plt.ylabel('Humidity (%)', fontsize=12)
plt.legend()
plt.grid(True, linestyle='--', alpha=0.3)
plt.tight_layout()
plt.show()

# 10. Print sample predictions
print("\nSample Predictions:")
print(results.head(10).to_string(index=False))