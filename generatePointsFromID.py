import csv
from gmplot import gmplot
from generateCoordinates import generateCoordsWithinSquare
import json
from pprint import pprint
import urllib
import urllib2
import os
import time

# Modify these to adjust box width and point count
meterWidth = 1000
count = 50
ID = "E0-001-107520878-7" #Event ID of interest, change this

def queryEventfulWithId(id):
	url = "http://api.eventful.com/json/events/get?app_key=srG2DMrq4VpRxGvw&id="+id
	response = urllib2.urlopen(url).read()
	rspJSON = json.loads(response)
	return rspJSON
	

# Open up json from eventful result
event = queryEventfulWithId(ID)
venue_name = event["venue_name"]
directory = "Venues/"+venue_name
latitude = float(event["latitude"])
longitude = float(event["longitude"])
gmap = gmplot.GoogleMapPlotter(latitude, longitude, 16)
map_file = directory+"/map.html"

# Store gps data to collect in a file, and visual map in map.html
if not os.path.exists(directory):
	os.makedirs(directory)
data = generateCoordsWithinSquare(latitude,longitude,meterWidth,count,gmap,map_file)
data["center_point"] = [latitude,longitude]
filename = directory + "/data_to_collect.json"
with open(filename, 'w') as fp:
	json.dump(data, fp, indent = 4, sort_keys=True)
