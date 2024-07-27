import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Daten laden
df = pd.read_csv('final_data.csv')

# Funktion zur Berechnung der Statistiken für ein gegebenes Höhenintervall
def calculate_statistics(df, lower_bound, upper_bound):
    df_filtered = df[(df['Altitude'] > lower_bound) & (df['Altitude'] <= upper_bound)]

    # Berechnung der Differenz zwischen Wind Speed Max und Wind Speed Min
    wind_speed_diff = df_filtered['Wind Speed Max (km/h)'] - df_filtered['Wind Speed Min (km/h)']

    stats = {
        'Lower Bound': lower_bound,
        'Upper Bound': upper_bound,
        'Average Wind Speed Min (km/h)': df_filtered['Wind Speed Min (km/h)'].mean(),
        'Average Wind Speed Avg (km/h)': df_filtered['Wind Speed Avg (km/h)'].mean(),
        'Average Wind Speed Max (km/h)': df_filtered['Wind Speed Max (km/h)'].mean(),
        'Average Wind Speed Diff (km/h)': wind_speed_diff.mean(),
        'Average Wind Heading (degrees)': df_filtered['Wind Heading (degrees)'].mean(),
        'Median Wind Speed Min (km/h)': df_filtered['Wind Speed Min (km/h)'].median(),
        'Median Wind Speed Avg (km/h)': df_filtered['Wind Speed Avg (km/h)'].median(),
        'Median Wind Speed Max (km/h)': df_filtered['Wind Speed Max (km/h)'].median(),
        'Median Wind Speed Diff (km/h)': wind_speed_diff.median(),
        'Median Wind Heading (degrees)': df_filtered['Wind Heading (degrees)'].median(),
        'Standard Deviation Wind Speed Min (km/h)': df_filtered['Wind Speed Min (km/h)'].std(),
        'Standard Deviation Wind Speed Avg (km/h)': df_filtered['Wind Speed Avg (km/h)'].std(),
        'Standard Deviation Wind Speed Max (km/h)': df_filtered['Wind Speed Max (km/h)'].std(),
        'Standard Deviation Wind Speed Diff (km/h)': wind_speed_diff.std(),
        'Standard Deviation Wind Heading (degrees)': df_filtered['Wind Heading (degrees)'].std()
    }

    return stats


stepSize = 50
# maxValue = int(df['Altitude'].max())
maxValue = 800

# Höhenintervalle berechnen und Statistiken sammeln
intervals = range(400, maxValue, stepSize)
statistics = []

for lower_bound in intervals:
    upper_bound = lower_bound + stepSize
    stats = calculate_statistics(df, lower_bound, upper_bound)
    statistics.append(stats)

# DataFrame mit den Ergebnissen erstellen
stats_df = pd.DataFrame(statistics)

# Plotten der Ergebnisse
plt.figure(figsize=(14, 12))

# Durchschnittswerte der Windgeschwindigkeit
plt.subplot(2, 2, 1)
plt.plot(stats_df['Upper Bound'], stats_df['Average Wind Speed Min (km/h)'], label='Avg Wind Speed Min (km/h)')
plt.plot(stats_df['Upper Bound'], stats_df['Average Wind Speed Avg (km/h)'], label='Avg Wind Speed Avg (km/h)')
plt.plot(stats_df['Upper Bound'], stats_df['Average Wind Speed Max (km/h)'], label='Avg Wind Speed Max (km/h)')
plt.plot(stats_df['Upper Bound'], stats_df['Average Wind Speed Diff (km/h)'], label='Avg Wind Speed Diff (km/h)')
plt.xlabel('Altitude (m)')
plt.ylabel('Wind Speed (km/h)')
plt.title('Average Wind Speed by Altitude')
plt.legend()

# Medianwerte der Windgeschwindigkeit
plt.subplot(2, 2, 2)
plt.plot(stats_df['Upper Bound'], stats_df['Median Wind Speed Min (km/h)'], label='Median Wind Speed Min (km/h)')
plt.plot(stats_df['Upper Bound'], stats_df['Median Wind Speed Avg (km/h)'], label='Median Wind Speed Avg (km/h)')
plt.plot(stats_df['Upper Bound'], stats_df['Median Wind Speed Max (km/h)'], label='Median Wind Speed Max (km/h)')
plt.xlabel('Altitude (m)')
plt.ylabel('Wind Speed (km/h)')
plt.title('Median Wind Speed by Altitude')
plt.legend()

# Standardabweichung der Windgeschwindigkeit
plt.subplot(2, 2, 3)
plt.plot(stats_df['Upper Bound'], stats_df['Standard Deviation Wind Speed Min (km/h)'], label='Std Dev Wind Speed Min (km/h)')
plt.plot(stats_df['Upper Bound'], stats_df['Standard Deviation Wind Speed Avg (km/h)'], label='Std Dev Wind Speed Avg (km/h)')
plt.plot(stats_df['Upper Bound'], stats_df['Standard Deviation Wind Speed Max (km/h)'], label='Std Dev Wind Speed Max (km/h)')
plt.plot(stats_df['Upper Bound'], stats_df['Standard Deviation Wind Speed Diff (km/h)'], label='Std Dev Wind Speed Diff (km/h)')
plt.xlabel('Altitude (m)')
plt.ylabel('Wind Speed (km/h)')
plt.title('Standard Deviation of Wind Speed by Altitude')
plt.legend()

# Durchschnittswerte der Windrichtung und Differenz
plt.subplot(2, 2, 4)
plt.plot(stats_df['Upper Bound'], stats_df['Average Wind Heading (degrees)'], label='Avg Wind Heading (degrees)')
plt.xlabel('Altitude (m)')
plt.ylabel('Value')
plt.title('Average Wind Heading and Wind Speed Difference by Altitude')
plt.legend()

plt.tight_layout()
plt.show()

stats_df.to_csv('stats_df.csv', index=False)

