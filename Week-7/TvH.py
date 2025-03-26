import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

# Load your data
df = pd.read_csv('Task_7.csv') 
X = df[['Temperature']].values
y = df['Humidity'].values

# Train the model
model = LinearRegression()
model.fit(X, y)

# Create test temperatures
test_temps = np.linspace(X.min(), X.max(), 100).reshape(-1, 1)
predicted_humidity = model.predict(test_temps)

# Calculate residuals (distance from points to trend line)
residuals = y - model.predict(X)

# Set up the plot
plt.figure(figsize=(12, 7))

# 1. Original data points
plt.scatter(X, y, color='blue', alpha=0.7, label='Actual Data', s=100)

# 2. Trend line
plt.plot(test_temps, predicted_humidity, 'r-', linewidth=3, label='Trend Line')

# 3. Highlight outliers (>2 standard deviations from trend)
std_dev = np.std(residuals)
outliers = np.abs(residuals) > 2 * std_dev
plt.scatter(X[outliers], y[outliers], color='orange', s=150, 
            edgecolor='black', linewidth=1.5, label='Outliers')

# Formatting
plt.title('Temperature vs Humidity Analysis', fontsize=16, pad=20)
plt.xlabel('Temperature (°C)', fontsize=14)
plt.ylabel('Humidity (%)', fontsize=14)
plt.legend(fontsize=12)
plt.grid(True, linestyle='--', alpha=0.3)
plt.tight_layout()

# Analysis results
print("=== Trend Line Analysis ===")
print(f"1. R-squared: {model.score(X, y):.4f} (1.0 = perfect fit)")
print(f"2. Trend equation: Humidity = {model.coef_[0]:.2f}*Temperature + {model.intercept_:.2f}")
print(f"3. Found {sum(outliers)} potential outliers (2σ threshold)")

# Show plot
plt.show()