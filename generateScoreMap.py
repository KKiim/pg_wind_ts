import pandas as pd
from datetime import datetime, timedelta
import json
import glob
import os
import bisect

# Cache für die Winddaten und geparsten Windzeiten
wind_data_cache = {}
wind_times_cache = {}

# Funktion zum Laden der Winddaten
def load_wind_data(file_path):
    with open(file_path, 'r') as f:
        data = json.load(f)
        return data['data']

# Laden aller Winddaten für einen bestimmten Monat mit Caching
def load_monthly_wind_data(year, month):
    cache_key = (year, month)
    if cache_key in wind_data_cache:
        return wind_data_cache[cache_key], wind_times_cache[cache_key]

    file_pattern = f'WindData_{year}-{str(month).zfill(2)}.json'
    file_paths = glob.glob(file_pattern)
    wind_data = []
    for file_path in file_paths:
        wind_data.extend(load_wind_data(file_path))

    wind_times = [datetime.strptime(entry[0], '%Y-%m-%dT%H:%M:%S.%fZ') for entry in wind_data]

    wind_data_cache[cache_key] = wind_data
    wind_times_cache[cache_key] = wind_times
    return wind_data, wind_times

# Funktion zum Zuordnen der Winddaten zu einem bestimmten Zeitpunkt
def find_wind_data_for_time(wind_data, wind_times, target_time):
    target_time = datetime.strptime(target_time, '%Y-%m-%dT%H:%M:%SZ')

    pos = bisect.bisect_left(wind_times, target_time)

    if pos == 0:
        closest_data = wind_data[0]
    elif pos == len(wind_times):
        closest_data = wind_data[-1]
    else:
        before = wind_times[pos - 1]
        after = wind_times[pos]
        if abs(before - target_time) <= abs(after - target_time):
            closest_data = wind_data[pos - 1]
        else:
            closest_data = wind_data[pos]

    return closest_data

# Funktion zum Verarbeiten einer IGC-Datei
def process_igc_file(file_path):
    with open(file_path, 'r') as f:
        lines = f.readlines()

    # Extrahieren der B-Datensätze
    b_records = [line.strip() for line in lines if line.startswith('B')]

    # Extrahieren des Datums
    date_record = next((line for line in lines if line.startswith('HFDTE')), None)
    if not date_record:
        return pd.DataFrame()

    date_str = date_record[5:].strip()
    flight_date = datetime.strptime(date_str, '%d%m%y').date()

    # Extrahieren der Zeit und Höhe
    data_list = []
    for record in b_records:
        time_str = record[1:7]
        altitude = int(record[30:35])
        time = datetime.strptime(time_str, '%H%M%S').time()
        datetime_utc = datetime.combine(flight_date, time)
        utc_string = datetime_utc.strftime('%Y-%m-%dT%H:%M:%SZ')
        data_list.append([utc_string, altitude])

    # Erstellen eines DataFrame
    df = pd.DataFrame(data_list, columns=['Time (UTC)', 'Altitude'])

    # Laden der Winddaten für den entsprechenden Monat
    year = flight_date.year
    month = flight_date.month
    wind_data, wind_times = load_monthly_wind_data(year, month)

    # Zuordnen der Winddaten zu jedem Zeitpunkt
    wind_speed_avg_list = []
    wind_speed_min_list = []
    wind_speed_max_list = []
    wind_heading_list = []
    for _, row in df.iterrows():
        wind_entry = find_wind_data_for_time(wind_data, wind_times, row['Time (UTC)'])
        wind_speed_avg = wind_entry[4] if wind_entry else None
        wind_speed_min = wind_entry[3] if wind_entry else None
        wind_speed_max = wind_entry[5] if wind_entry else None
        wind_heading = wind_entry[6] if wind_entry else None
        wind_speed_avg_list.append(wind_speed_avg)
        wind_speed_min_list.append(wind_speed_min)
        wind_speed_max_list.append(wind_speed_max)
        wind_heading_list.append(wind_heading)

    # Hinzufügen der Winddaten zum DataFrame
    df['Wind Speed Avg (km/h)'] = wind_speed_avg_list
    df['Wind Speed Min (km/h)'] = wind_speed_min_list
    df['Wind Speed Max (km/h)'] = wind_speed_max_list
    df['Wind Heading (degrees)'] = wind_heading_list

    return df

# Verzeichnis der IGC-Dateien
igc_directory = r'C:\Users\Kim\source\repos\RadoApp\src\assets'

# Verarbeiten aller IGC-Dateien im Verzeichnis und Unterverzeichnissen
all_dfs = []
for file_path in glob.glob(os.path.join(igc_directory, '**', '*.igc'), recursive=True):
    print(file_path)
    df = process_igc_file(file_path)
    print(df)
    if not df.empty:
        all_dfs.append(df)

# Kombinieren aller DataFrames
final_df = pd.concat(all_dfs, ignore_index=True)

# Speichern des DataFrame als CSV-Datei
final_df.to_csv('final_data.csv', index=False)

# Laden des DataFrame aus der CSV-Datei
loaded_df = pd.read_csv('final_data.csv')

# Ausgabe des finalen DataFrame
print(loaded_df)
