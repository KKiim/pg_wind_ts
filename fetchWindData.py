import requests
import json
from datetime import datetime

def fetch_wind_data(year, month):
    try:
        # Ensure the month is in the correct format (two digits)
        month_str = f"{int(month):02d}"

        # Calculate the stop date (the next month)
        start_date = f"{year}-{month_str}"
        if int(month) == 12:
            stop_date = f"{int(year) + 1}-01"
        else:
            stop_date = f"{year}-{int(month) + 1:02d}"

        # Generate the URL
        url = f"https://api.pioupiou.fr/v1/archive/1339?start={start_date}&stop={stop_date}"

        # Fetch the data from the URL
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()

            # Define the filename
            filename = f"WindData_{start_date}.json"

            # Save the data to a JSON file
            with open(filename, 'w') as file:
                json_str = json.dumps(data, separators=(',', ':'))
                json_str = json_str.replace('],', '],\n')
                file.write(json_str)


            print(f"Data saved to {filename}")
        else:
            print(f"Failed to retrieve data. HTTP Status Code: {response.status_code}")
    except Exception as e:
        print(f"An error occurred: {e}")

# Get user input for year and month
year = input("Enter the year (e.g., 2024): ")
month = input("Enter the month (e.g., 03): ")

# Fetch and save the wind data
fetch_wind_data(year, month)
