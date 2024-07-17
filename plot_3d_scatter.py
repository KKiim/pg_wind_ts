import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

# Load the data
df = pd.read_csv('final_data.csv')

# Extract the necessary columns
altitude = df['Altitude']
wind_speed_avg = df['Wind Speed Avg (km/h)']
wind_speed_max = df['Wind Speed Max (km/h)']

# Create a 3D scatter plot
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Plot with color gradient based on log of altitude
sc = ax.scatter(wind_speed_avg, wind_speed_max, altitude, c=np.log10(altitude), cmap='viridis')

# Add color bar which maps values to colors
cbar = plt.colorbar(sc, ax=ax, pad=0.1)
cbar.set_label('Log10(Altitude)')

# Set labels
ax.set_xlabel('Wind Speed Avg (km/h)')
ax.set_ylabel('Wind Speed Max (km/h)')
ax.set_zlabel('Altitude (log scale)')

# Set log scale for altitude
ax.set_zscale('log')

# Set title
ax.set_title('3D Scatter Plot of Flight Data')

# Show plot
plt.show()
