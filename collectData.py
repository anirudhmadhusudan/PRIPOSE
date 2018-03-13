import urllib
import json
import urllib2
import os
import time
import csv


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
		return [str(lat),str(lon),str(freeFlowSpeed),str(currentSpeed),str(ratio),str(confidence),str(time.time())]
	except urllib2.HTTPError as err:
		return "Not found"

# One sample from every coordinate we have

def collect_sample():
	rootdir = "Venues/"
	for folder in os.listdir(rootdir):
		filename = rootdir+"/"+folder+"/data_to_collect.json"
		with open(filename, 'r') as fp:
			with open(rootdir+"/"+folder+'/data.csv', 'w') as csvfile:
				spamwriter = csv.writer(csvfile, delimiter=',')
				data = json.load(fp)
				sample_points = data["sample_points"]
				print filename
				for sample_point in sample_points:
					latitude = str(sample_point[0])
					longitude = str(sample_point[1])
					entry = getSpeedAtLoc(latitude,longitude)
					if entry != "Not found":
						spamwriter.writerow(entry)

while(1):
	collect_sample
	print("Collecting a sample")
	time.sleep(900) #sleep for 15 minutes