import pandas as pd
from sklearn.linear_model import LinearRegression
import numpy as np

# Lesen der Daten aus height2measurement.csv
df = pd.read_csv('height2measurement.csv')

# Konvertieren der Zeitstempel in datetime-Objekte
df['Time (UTC)'] = pd.to_datetime(df['Time (UTC)'])
df['Wind Ts'] = pd.to_datetime(df['Wind Ts'])

# Sortieren der Daten nach Zeitstempel
df = df.sort_values('Time (UTC)')

# Initialisieren der Liste für die Ergebnisse
results = []

# Berechnung des Höhenunterschieds für jeden Windmesszeitpunkt
for wind_ts in df['Wind Ts'].unique():
    # Filter für die Daten vor und nach dem aktuellen Windmesszeitpunkt
    current_df = df[df['Wind Ts'] == wind_ts]

    # Extraktion der relevanten Daten für die Regression
    X = (current_df['Time (UTC)'] - current_df['Time (UTC)'].min()).dt.total_seconds().values.reshape(-1, 1)
    y = current_df['Altitude'].values

    # Überprüfen, ob genügend Datenpunkte vorhanden sind
    if len(y) > 1:
        # Anwendung der linearen Regression
        model = LinearRegression().fit(X, y)
        # Berechnung der Steigung (Höhenänderung pro Sekunde)
        altitude_delta_per_sec = model.coef_[0]
    else:
        altitude_delta_per_sec = np.nan  # nicht genug Datenpunkte

    # Bestimmen der maximalen Höhe in diesem Intervall
    max_altitude = current_df['Altitude'].max()

    # Hinzufügen der Ergebnisse zur Liste
    results.append({
        'Wind Ts': wind_ts,
        'Altitude': max_altitude,
        'Wind Speed Avg (km/h)': current_df['Wind Speed Avg (km/h)'].iloc[0],
        'Wind Speed Min (km/h)': current_df['Wind Speed Min (km/h)'].iloc[0],
        'Wind Speed Max (km/h)': current_df['Wind Speed Max (km/h)'].iloc[0],
        'Wind Heading (degrees)': current_df['Wind Heading (degrees)'].iloc[0],
        'Altitude Delta (m/s)': altitude_delta_per_sec
    })

# Erstellen des DataFrame für die Ergebnisse
results_df = pd.DataFrame(results)

# Speichern der Ergebnisse in altitude_delta.csv
results_df.to_csv('final_data.csv', index=False)

print("Ergebnisse wurden in final_data.csv gespeichert.")
