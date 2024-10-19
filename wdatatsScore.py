import pandas as pd
from datetime import datetime, timedelta

# Load data from CSV file
data = pd.read_csv('C:\\Users\\Kim\\source\\repos\\RadoApp\\public\\height2measurement.csv')

# Convert Time (UTC) and Wind Ts columns to datetime
data['Time (UTC)'] = pd.to_datetime(data['Time (UTC)'], format='%Y-%m-%dT%H:%M:%SZ')
data['Wind Ts'] = pd.to_datetime(data['Wind Ts'], format='%Y-%m-%dT%H:%M:%S.%fZ')

# Initialize variables
all_intervals = []

# Process data
i = 0
while i < len(data):
    interval_start = data.loc[i, 'Time (UTC)']
    interval_end = interval_start + timedelta(seconds=120)
    interval_data = data[(data['Time (UTC)'] >= interval_start) & (data['Time (UTC)'] <= interval_end)]

    if not interval_data.empty:
        start_altitude = interval_data.iloc[0]['Altitude']
        end_altitude = interval_data.iloc[-1]['Altitude']
        min_altitude = interval_data['Altitude'].min()
        max_altitude = interval_data['Altitude'].max()

        # Calculate the net rise in the interval
        net_rise = end_altitude - start_altitude if end_altitude > start_altitude else 0

        interval_info = interval_data.iloc[-1].to_dict()
        interval_info['Score'] = net_rise

        if all_intervals and all_intervals[-1]['Wind Ts'] == interval_info['Wind Ts']:
            if all_intervals[-1]['Score'] < interval_info['Score']:
                all_intervals[-1]['Score'] = interval_info['Score']
        else:
            all_intervals.append(interval_info)

    # Move to the next data point after the current interval
    i += 1
    while i < len(data) and data.loc[i, 'Time (UTC)'] <= interval_end:
        i += 1

# Create a DataFrame for all intervals
all_data = pd.DataFrame(all_intervals)

# Save to CSV
all_data.to_csv('heightGainData_with_hm_scores.csv', index=False)
