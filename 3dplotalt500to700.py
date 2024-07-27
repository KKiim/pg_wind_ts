import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

# Load the data
df = pd.read_csv('final_data.csv')

# Filter the data for altitude between 500 and 700
df_filtered = df[(df['Altitude'] > 480) & (df['Altitude'] < 1000)]

# Extract the necessary columns
altitude = df_filtered['Altitude']
wind_speed_avg = df_filtered['Wind Speed Avg (km/h)']
wind_speed_max = df_filtered['Wind Speed Max (km/h)']

# Function to add jitter
def jitter(val):
    return val + (np.random.rand(len(val)) - 0.5) * 5

# Create a 3D scatter plot
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Plot with jitter
sc = ax.scatter(jitter(wind_speed_avg), jitter(wind_speed_max), jitter(altitude), c=altitude, cmap='viridis')

# Add color bar which maps values to colors
cbar = plt.colorbar(sc, ax=ax, pad=0.01)
cbar.set_label('Altitude')

# Set labels
ax.set_xlabel('Wind Speed Avg (km/h)')
ax.set_ylabel('Wind Speed Max (km/h)')
ax.set_zlabel('Altitude')

# Set title
ax.set_title('3D Scatter Plot of Flight Data')

# Show plot
plt.show()
