
# coding: utf-8

# In[ ]:


import csv
from gmplot import gmplot
import json
from pprint import pprint
import urllib.request  as urllib2 
import os
import time
import math
import random

key = "RzxaJBZ093ilm9BRpsuMWX8AiYTmc8kN"
EARTH_POLAR_RADIUS_METER = 6356800
EARTH_EQUATORIAL_RADIUS_METER = 6378100
meterWidth = 1000
count = 50

def queryEventfulWithId(id):
	url = "http://api.eventful.com/json/events/get?app_key=srG2DMrq4VpRxGvw&id="+id
	response = urllib2.urlopen(url).read()
	rspJSON = json.loads(response)
	return rspJSON
    
# Gets the metric length corresponding to the latitude, in degrees.
def getLatitudeWidth(meterWidth):
    return meterWidth/(2*math.pi*EARTH_POLAR_RADIUS_METER ) *360

# Convert the metric width to the corresponding longitude width at latitude
def getLongitudeWidthAtLatitue(latitude, meterWidth):
    circleMeterLengthAtLatitude = 2 * math.pi * EARTH_EQUATORIAL_RADIUS_METER * math.cos(latitude / 180 * math.pi)
    return meterWidth/circleMeterLengthAtLatitude * 360

def degreesToRadians(degrees):
	return degrees * math.pi / 180

def distanceInMetersBetweenEarthCoordinates(lat1, lon1, lat2, lon2):
	earthRadiusKm = 6371
	dLat = degreesToRadians(lat2-lat1)
	dLon = degreesToRadians(lon2-lon1)
	lat1 = degreesToRadians(lat1)
	lat2 = degreesToRadians(lat2)
	a = math.sin(dLat/2) * math.sin(dLat/2) + math.sin(dLon/2) * math.sin(dLon/2) * math.cos(lat1) * math.cos(lat2) 
	c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a)) 
	return earthRadiusKm * c * 1000


# Generates a uniform distribution of count coordinates
# Boundary defined by lat,lon of center corner and width in meters
def generateCoordsWithinSquare(centerLat,centerLon,meterWidth,count,gmap,map_file):

	# Generate rectangle width in latitude and longitude coordinates
	dLat = getLatitudeWidth(meterWidth)
	dLon = getLongitudeWidthAtLatitue(centerLat,meterWidth)

	# Generate and show rectangle boundaries
	upperLeftLat = centerLat + (dLat / 2.0)
	upperLeftLon = centerLon - (dLon / 2.0)

	lowerRightLat = upperLeftLat - dLat
	lowerRightLon = upperLeftLon + dLon

	upperRightLat = upperLeftLat
	upperRightLon = lowerRightLon

	lowerLeftLat = lowerRightLat
	lowerLeftLon = upperLeftLon

	latitudes = []
	longitudes = []
	distances_to_center = []

	# Generate count randomly distributed coordinates
	for i in range(count):
		lat = random.uniform(upperLeftLat, lowerLeftLat)
		lon = random.uniform(upperLeftLon, upperRightLon)
		dist = distanceInMetersBetweenEarthCoordinates(centerLat,centerLon,lat,lon)
		latitudes.append(lat)
		longitudes.append(lon)
		distances_to_center.append(dist)
        
	boundaries = [[upperLeftLat, upperRightLat, lowerRightLat, lowerLeftLat, upperLeftLat], [upperLeftLon, upperRightLon, lowerRightLon, lowerLeftLon, upperLeftLon]]

	return latitudes,longitudes,distances_to_center

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
        print ("not found")



import pandas as pd
columns = ['event','title','venue','venue_lat','venue_lon','sample_lats','sample_lons','sample_dist']
df = pd.DataFrame(columns=columns)



######EDIT ME########## 

# In the string belong change the date from name to the csv file name

df = pd.read_csv("March24_Richard and Karen Carpenter Performing Arts Center.csv")


counter = 0
while counter <= 11:
    columns1 = ['eventname','loc_type','lat','lon','freeflowspeed','currentspeed','ratio','confidence','CST Time','dist_from_center']
    i = 0
    dfadd = pd.DataFrame([['ignore this row',"2",1.1,1.1,21,21,1,1,1,0]],columns=columns1)


    for i in range(1):
        loc_type = "C"
        lat = df['venue_lat'][i]
        lon = df['venue_lon'][i]
        lat,lon,freeFlowSpeed,currentSpeed,ratio,confidence,timeticks = getSpeedAtLoc(str(lat),str(lon))
        dfadd.loc[len(dfadd)]= [str(df['title'][i]),loc_type,lat,lon,freeFlowSpeed,currentSpeed,ratio,confidence,time.ctime(int(float((timeticks)))),0]

        for j in range(50):
            loc_type = "S"
            lat,lon,freeFlowSpeed,currentSpeed,ratio,confidence,timeticks = getSpeedAtLoc(str(df['sample_lats'][i][j]),str(df['sample_lons'][i][j]))
            dfadd.loc[len(dfadd)] = [str(df['title'][i]),loc_type,lat,lon,freeFlowSpeed,currentSpeed,ratio,confidence,time.ctime(int(float((timeticks)))),df['sample_dist'][i][j]]

    ######EDIT ME##########
    
    # In the string belong change the date from March24 to whatever date it is.    
    
    dfadd.to_csv('March24_' + venue_name + str(time.ctime(int(float((timeticks))))) + '.csv')
    if counter == 11:
        break
    time.sleep(1800)
    counter += 1

