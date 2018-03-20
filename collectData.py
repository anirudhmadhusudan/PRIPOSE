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

		#TODO: put average of returned segments lat and lon here

		return [str(lat),str(lon),str(freeFlowSpeed),str(currentSpeed),str(ratio),str(confidence),str(time.time())]
	except urllib2.HTTPError as err:
		return "Not found"

# One sample from every coordinate we have

def collect_sample():
	rootdir = "Venues/"
	for folder in os.listdir(rootdir):
		filename = rootdir+"/"+folder+"/data_to_collect.json"
		with open(filename, 'r') as fp:
			with open(rootdir+"/"+folder+'/data.csv', 'a') as csvfile:
				spamwriter = csv.writer(csvfile, delimiter=',')
				data = json.load(fp)
				sample_points = data["sample_points"]
				print sample_points
				print filename
				for sample_point in sample_points:
					latitude = str(sample_point[0])
					longitude = str(sample_point[1])
					entry = getSpeedAtLoc(latitude,longitude)
					if entry != "Not found":
						spamwriter.writerow(entry)

def collect_sample_with_venue(venue):
	rootdir = "Venues/"
	filename = rootdir+venue+"/data_to_collect.json"
	with open(filename, 'r') as fp:
		with open(rootdir+"/"+venue+'/data.csv', 'a') as csvfile:
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

# while(1):
# 	collect_sample()
# 	print("Collecting a sample")
# 	time.sleep(1800) #sleep for 30 minutes

# # Or just call collect_sample once
# collect_sample()

# Or collect sample from just a venue
collect_sample_with_venue("The Kent Stage")