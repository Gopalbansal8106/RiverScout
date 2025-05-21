import osmnx as ox
import geopandas as gpd
import numpy as np
import csv
from shapely.geometry import LineString, MultiLineString

# Define bounding box (Varanasi region)
north = 25.45
south = 25.15
east = 83.1
west = 82.9

# Define tags for rivers
tags = {"waterway": "river"}

# Correct function call - ONLY POSITIONAL args
rivers = ox.features.features_from_bbox(north, south, east, west, tags)

# Filter Ganga by name
ganga = rivers[rivers["name"].str.contains("Ganga", case=False, na=False)]

# Merge to single geometry
geometry = ganga.geometry.unary_union

# Choose the longest LineString if it's a MultiLineString
if isinstance(geometry, MultiLineString):
    geometry = max(geometry.geoms, key=lambda g: g.length)

# Function to sample points along the river every 500 meters
def sample_line(line, interval=500):
    distances = np.arange(0, line.length, interval)
    return [line.interpolate(d) for d in distances]

points = sample_line(geometry, interval=500)

# Extract lat, lon pairs
coords = [(pt.y, pt.x) for pt in points]

# Save to CSV
with open("ganga_varanasi_coords.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["latitude", "longitude"])
    writer.writerows(coords)

print(f"Saved {len(coords)} coordinates to ganga_varanasi_coords.csv")




