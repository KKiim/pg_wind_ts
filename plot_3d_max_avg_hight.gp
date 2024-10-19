# Set the terminal to PNG or your desired output format
set terminal pngcairo size 800,600 enhanced

set output 'scatter_plot_3d.png'

# Set datafile separator
set datafile separator ','

# Set labels and title
set title "3D Scatter Plot of Flight Data"
set xlabel "Wind Speed Avg (km/h)"
set ylabel "Wind Speed Max (km/h)"
set zlabel "Altitude"

# Set the point size smaller
set pointsize 1

# Enable grid
set grid

# Define the color palette
set palette defined (0 "blue", 1 "green", 2 "yellow", 3 "orange", 4 "red")

# Function to add jitter
jitter(val) = val + (rand(0) - 0.5) * 5

# Plot the data as points (3D scatter plot) with jitter and color gradient based on altitude
splot "final_data.csv" using (jitter($3)):(jitter($5)):(jitter($2)):(jitter($2)) with points pointtype 7 palette title "Altitude"
