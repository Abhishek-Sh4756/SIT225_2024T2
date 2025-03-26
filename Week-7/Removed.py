import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

# Load data
df = pd.read_csv('Task_7.csv')  

# 1. Initial Analysis
print("=== Initial Data Summary ===")
print(f"Original data points: {len(df)}")
print(df[['Temperature', 'Humidity']].describe())

# 2. Visualize original distribution
plt.figure(figsize=(12, 5))
plt.subplot(1, 2, 1)
plt.boxplot(df['Temperature'], vert=False)
plt.title('Original Temperature Distribution')
plt.xlabel('°C')

# 3. Filter temperature outliers using IQR method
Q1 = df['Temperature'].quantile(0.25)
Q3 = df['Temperature'].quantile(0.75)
IQR = Q3 - Q1

# Define bounds (adjust multiplier as needed)
lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR

# Filter dataframe
filtered_df = df[(df['Temperature'] >= lower_bound) & 
                 (df['Temperature'] <= upper_bound)].copy()

print("\n=== Filtered Data Summary ===")
print(f"Removed {len(df) - len(filtered_df)} outliers")
print(f"Remaining data points: {len(filtered_df)}")
print(filtered_df[['Temperature', 'Humidity']].describe())

# 4. Visualize filtered distribution
plt.subplot(1, 2, 2)
plt.boxplot(filtered_df['Temperature'], vert=False)
plt.title('Filtered Temperature Distribution')
plt.xlabel('°C')
plt.tight_layout()
plt.show()

# 5. Train new model with filtered data
X = filtered_df[['Temperature']].values
y = filtered_df['Humidity'].values

model = LinearRegression()
model.fit(X, y)

# 6. Create predictions
test_temps = np.linspace(X.min(), X.max(), 100).reshape(-1, 1)
predicted_humidity = model.predict(test_temps)

# 7. Plot comparison
plt.figure(figsize=(12, 7))

# Original data (light blue)
plt.scatter(df['Temperature'], df['Humidity'], 
            color='lightblue', alpha=0.5, label='Original Data')

# Filtered data (dark blue)
plt.scatter(filtered_df['Temperature'], filtered_df['Humidity'], 
            color='blue', alpha=0.7, label='Filtered Data')

# New trend line
plt.plot(test_temps, predicted_humidity, 'r-', linewidth=3, label='New Trend Line')

plt.title('Temperature vs Humidity: Before/After Outlier Removal', fontsize=16)
plt.xlabel('Temperature (°C)', fontsize=14)
plt.ylabel('Humidity (%)', fontsize=14)
plt.legend(fontsize=12)
plt.grid(True, linestyle='--', alpha=0.3)
plt.show()

# 8. Compare model performance
print("\n=== Model Comparison ===")
print(f"Original R-squared: {LinearRegression().fit(df[['Temperature']], df['Humidity']).score(df[['Temperature']], df['Humidity']):.4f}")
print(f"Filtered R-squared: {model.score(X, y):.4f}")
print(f"New trend equation: Humidity = {model.coef_[0]:.2f}*Temperature + {model.intercept_:.2f}")