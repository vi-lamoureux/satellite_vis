import csv
from datetime import datetime, timedelta, timezone
from skyfield.api import load

# Load satellites data
satellites_url = 'http://celestrak.com/NORAD/elements/active.txt'
satellites = load.tle_file(satellites_url)

# Load timescale
ts = load.timescale()

# Define end time as midnight of the current day (in UTC timezone)
current_time = datetime.now(timezone.utc)
end_time = current_time.replace(hour=0, minute=0, second=0, microsecond=0)

# Subtract 101 days to get the start time
start_time = end_time - timedelta(days=101)

# Generate list of hours
hours = [start_time + timedelta(hours=n) for n in range(101*24)]  # 101 days * 24 hours per day

# Open CSV file
with open('satellite_positions_hourly.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['Satellite', 'Time', 'Latitude', 'Longitude', 'Elevation'])

    # For each satellite
    for satellite in satellites:
        # For each hour
        for hour in hours:
            # Calculate satellite position using interpolation
            geocentric = satellite.at(ts.utc(hour))
            subpoint = geocentric.subpoint()

            # Write data to CSV
            writer.writerow([satellite.name, hour.strftime('%Y-%m-%d %H:%M:%S'), subpoint.latitude.degrees, subpoint.longitude.degrees, subpoint.elevation.m])