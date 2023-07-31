import csv
from tqdm import tqdm
from skyfield.api import load

# Load satellites data
satellites_url = 'http://celestrak.com/NORAD/elements/active.txt'
satellites = load.tle_file(satellites_url)
by_name = {sat.name: sat for sat in satellites}

# Load timescale
ts = load.timescale()

# Define start and end times
end_time = ts.now()
start_time = end_time + 100 # adds 100 days

# Generate list of days
days = [start_time + n for n in range(101)]  # 101 days including start and end

# Open CSV file
with open('projected_satellite_positions.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['Satellite', 'Time', 'Latitude', 'Longitude', 'Elevation'])

    # For each satellite
    for name, sat in tqdm(by_name.items(), total=len(by_name)):
        # For each day
        for day in days:
            # Calculate satellite position
            geocentric = sat.at(day)
            subpoint = geocentric.subpoint()

            # Write data to CSV
            writer.writerow([name, day.utc_strftime('%Y-%m-%d'), subpoint.latitude.degrees, subpoint.longitude.degrees, subpoint.elevation.m])
