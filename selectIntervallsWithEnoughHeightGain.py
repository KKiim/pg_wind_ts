import pandas as pd
from datetime import datetime, timedelta

# Load data from CSV file
data = pd.read_csv('height2measurement.csv')

# Convert Time (UTC) and Wind Ts columns to datetime
data['Time (UTC)'] = pd.to_datetime(data['Time (UTC)'], format='%Y-%m-%dT%H:%M:%SZ')
data['Wind Ts'] = pd.to_datetime(data['Wind Ts'], format='%Y-%m-%dT%H:%M:%S.%fZ')

# Initialize variables
interval_start = None
interval_end = None
start_altitude = None
all_intervals = []

# Process data
for i in range(len(data) - 1):
    current_time = data.loc[i, 'Time (UTC)']
    next_time = data.loc[i + 1, 'Time (UTC)']

    if interval_start is None:
        interval_start = current_time
        start_altitude = data.loc[i, 'Altitude']

    # Check if the next data point is exactly one second after the current
    if (next_time - current_time).total_seconds() == 1:
        current_altitude = data.loc[i + 1, 'Altitude']
        altitude_gain = current_altitude - start_altitude

        # Check if altitude gain exceeds 60 meters within 120 seconds
        if altitude_gain >= 40 and (next_time - interval_start).total_seconds() <= 120:
            interval_end = next_time
            interval_data = data.loc[i + 1].to_dict()
            interval_data['Score'] = 1
            if all_intervals[-2]['Wind Ts'] == interval_data['Wind Ts']:
                continue
            all_intervals.append(interval_data)
            interval_start = None
            start_altitude = None
        elif (next_time - interval_start).total_seconds() > 120:
            interval_end = next_time
            interval_data = data.loc[i + 1].to_dict()
            interval_data['Score'] = 0
            all_intervals.append(interval_data)
            interval_start = current_time
            start_altitude = data.loc[i, 'Altitude']
    else:
        interval_end = current_time
        interval_data = data.loc[i].to_dict()
        interval_data['Score'] = 0
        all_intervals.append(interval_data)
        interval_start = current_time
        start_altitude = data.loc[i, 'Altitude']

# Handle the last interval
if interval_start is not None:
    interval_data = data.iloc[-1].to_dict()
    interval_data['Score'] = 0
    all_intervals.append(interval_data)

# Create a DataFrame for all intervals
all_data = pd.DataFrame(all_intervals)

all_data.to_csv('heightGainData_with_scores.csv', index=False)
