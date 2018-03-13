import urllib
import json
import urllib2
import os
import time


key = "4BGs4umzWE9Bg7fluGQR7gToO6Qlageu"

# Returns live traffic data from TomTom API call
def getSpeedAtLoc(lat,lon):
	try:
		url = "https://api.tomtom.com/traffic/services/4/flowSegmentData/absolute/10/json?key="+key+"&point="+lat+","+lon+"&unit=MPH"
		response = urllib2.urlopen(url).read()
		rspJSON = json.loads(response)
		data = rspJSON['flowSegmentData']
		freeFlowSpeed = data["freeFlowSpeed"]
		currentSpeed = data["currentSpeed"]
		confidence = data["confidence"]
		ratio = round(currentSpeed/float(freeFlowSpeed),2)
		return str(lat)+", "+str(lon)+", "+str(freeFlowSpeed)+", "+str(currentSpeed)+", "+str(ratio)+", "+str(confidence)+", "+str(time.time())
	except urllib2.HTTPError as err:
		print("Not found")

# Main
rootdir = "Venues/"
for folder in os.listdir(rootdir):
	filename = rootdir+"/"+folder+"/data_to_collect.json"
	with open(filename, 'r') as fp:
		data = json.load(fp)
		sample_points = data["sample_points"]
		lats = sample_points[0]
		lons = sample_points[1]
		for i in range(len(lats)):
			latitude = str(lats[i])
			longitude = str(lons[i])
			print(getSpeedAtLoc(latitude,longitude))
			break
	break

