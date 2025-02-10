import pandas as pd
import matplotlib.pyplot as plt



data = pd.read_csv("Final.csv")


print(data.head())

# Plot the data
plt.figure(figsize=(10, 6))


plt.plot(data['time'], data['xvalue'], label='X Value', color='r')
plt.plot(data['time'], data['yvalue'], label='Y Value', color='g')
plt.plot(data['time'], data['zvalue'], label='Z Value', color='b')

# Add labels and title
plt.xlabel('Time')
plt.ylabel('Value')
plt.title('X, Y, Z values over Time')
plt.legend()

# Show the plot
plt.grid(True)
plt.tight_layout()
plt.show()

