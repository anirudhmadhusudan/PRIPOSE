import csv
import time
import math
from gmplot import gmplot
import random


EARTH_POLAR_RADIUS_METER = 6356800
EARTH_EQUATORIAL_RADIUS_METER = 6378100



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


	sample_points = zip(latitudes,longitudes)
	boundaries = [[upperLeftLat, upperRightLat, lowerRightLat, lowerLeftLat, upperLeftLat], [upperLeftLon, upperRightLon, lowerRightLon, lowerLeftLon, upperLeftLon]]
	# Plot center coordinate
	gmap.scatter([centerLat],[centerLon],color="#ff0000")

	# Plot scattered sampling coordinates
	gmap.scatter(latitudes,longitudes,color="#000000")

	# Plot bounding rectangle
	gmap.plot(boundaries[0], boundaries[1])
	gmap.draw(map_file)
	return {"boundary": boundaries, "sample_points": sample_points, "distances_to_center": distances_to_center}
	