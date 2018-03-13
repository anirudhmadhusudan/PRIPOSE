import csv
from gmplot import gmplot
from generateCoordinates import generateCoordsWithinSquare
import json
from pprint import pprint
import os

meterWidth = 5000
count = meterWidth / 30

# Open up json from eventful result
data = json.load(open('EventfulQueries/nextWeek200Popular.json'))
events = data["events"]["event"]
for event in events:
	venue_name = event["venue_name"]
	directory = "Venues/"+venue_name
	latitude = float(event["latitude"])
	longitude = float(event["longitude"])
	gmap = gmplot.GoogleMapPlotter(latitude, longitude, 13)
	map_file = directory+"/map.html"

	# Store gps data to collect in a file, and visual map in map.html
	if not os.path.exists(directory):
		os.makedirs(directory)
	data = generateCoordsWithinSquare(latitude,longitude,meterWidth,count,gmap,map_file)
	data["center_point"] = [latitude,longitude]
	filename = directory + "/data_to_collect.json"
	with open(filename, 'w') as fp:
		json.dump(data, fp, indent = 4, sort_keys=True)
