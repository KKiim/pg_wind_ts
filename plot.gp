# Set the terminal to PNG or your desired output format
set terminal pngcairo size 3200,2400 enhanced

set output 'scatter_plot.png'

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
plot "final_data.csv" using (jitter($2)):(jitter($3)) with points pointtype 7 lc rgb "blue" title "Wind Speed Avg (km/h)", \
     "final_data.csv" using (jitter($2)):(jitter($4)) with points pointtype 7 lc rgb "red" title "Wind Speed Min (km/h)", \
     "final_data.csv" using (jitter($2)):(jitter($5)) with points pointtype 7 lc rgb "green" title "Wind Speed Max (km/h)"