import csv
from datetime import datetime, timedelta, timezone
from skyfield.api import load

# Load satellites data
satellites_url = 'http://celestrak.com/NORAD/elements/active.txt'
satellites = load.tle_file(satellites_url)

# Load timescale
ts = load.timescale()

# Define the specific date for which you want positions (in UTC timezone)
specific_date = datetime(2023, 7, 1, 0, 0, 0, tzinfo=timezone.utc)

# Generate list of 15-minute intervals for the specific date
time_interval = timedelta(minutes=15)
timestamps = [specific_date + n*time_interval for n in range(24*4)]  # 24 hours * 4 intervals per hour (15 minutes)

# Open CSV file
with open('satellite_positions_15min_1july2023.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['Satellite', 'Time', 'Latitude', 'Longitude', 'Elevation'])

    # For each satellite
    for satellite in satellites:
        # For each 15-minute interval on the specific date
        for timestamp in timestamps:
            # Calculate satellite position using interpolation
            geocentric = satellite.at(ts.utc(timestamp))
            subpoint = geocentric.subpoint()

            # Write data to CSV
            writer.writerow([satellite.name, timestamp.strftime('%Y-%m-%d %H:%M:%S'), subpoint.latitude.degrees, subpoint.longitude.degrees, subpoint.elevation.m])
