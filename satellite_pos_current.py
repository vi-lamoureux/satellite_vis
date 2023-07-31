import csv
from datetime import datetime, timedelta
from skyfield.api import Topos, load

# Load satellites data
stations_url = 'http://celestrak.com/NORAD/elements/stations.txt'
satellites = load.tle_file(stations_url)
by_name = {sat.name: sat for sat in satellites}

# Load timescale
ts = load.timescale()

# Define start and end times
end_time = ts.now()
start_time = end_time - 100 # subtracts 100 days

# Generate list of days
days = [start_time + n for n in range(101)]  # 101 days including start and end

# Open CSV file
with open('satellite_positions.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['Satellite', 'Time', 'Latitude', 'Longitude', 'Elevation'])

    # For each satellite
    for name, sat in by_name.items():
        # For each day
        for day in days:
            # Calculate satellite position
            geocentric = sat.at(day)
            subpoint = geocentric.subpoint()

            # Write data to CSV
            writer.writerow([name, day.utc_strftime('%Y-%m-%d'), subpoint.latitude.degrees, subpoint.longitude.degrees, subpoint.elevation.m])
