# Set the terminal to PNG or your desired output format
set terminal pngcairo size 3200,2400 enhanced

set output 'scatter_plot_dir.png'

# Set datafile separator
set datafile separator ','

# Set labels and title
set title "Flight Data Scatter Plot"
set xlabel "Altitude"
set ylabel "Values"

# Set the point size smaller
set pointsize 0.1

# Function to add jitter
jitter(val) = val + (rand(0) - 0.5) * 5

# Plot the data as points (scatter plot) with jitter
plot "final_data.csv" using (jitter($2)):(jitter($6)) with points pointtype 7 lc rgb "purple" title "Wind Heading (degrees)"
