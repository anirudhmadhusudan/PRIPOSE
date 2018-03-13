Live Data Collection Setup

Before running anything, look in the Venues folder. The idea for this is that each folder contains a venue of a popular event taken from eventful. Here, all of the data taken around that venue will be stored here. Right now, there is a map that has the boundary around the venue (5 km square) and a bunch of randomly generated sample points we will be feeding into the Tom tom api. 

If you want to run everything, here are the steps: 

1) Go to a browser and visit the url in SearchQuery.txt
2) Copy and Paste the result into http://jsbeautifier.org/ to pretty print the json file
3) Save that file as "nextWeek200Popular.json" and store it in EventfulQueries directory
	- These steps only need to be performed once
	- This gets the top 200 events from next week sorted by popularity
4) run generateVenuesToCollect.py
	This will:
		- Create a list of venues from the eventful query
		- Get the gps coordinate of each venue
		- Generate a bounding box and 5000 sample coordinates per venue
		- Generate a map.html to visualize these points
		- Store the center, bounding box, and sample points in a json file
5) run collectData.py
	This will (eventually):
		- Go through all of the sample points and call the TomTom api to get various measurements for the sample point
		- Record this in a file in the corresponding venue folder
		- Needs to run all the time (I have a raspberry pi we can use), and periodically

Notes
	- The free version of the tomtom api only allows 2.5k queries per day
	- we need way more than this, may have to pay, should talk to prof
	- Each measurement of the tom tom api has the current speed as well as "free flow traffic"
		- free flow traffic is what the speed should be in ideal situations, this can be helpful
	- The eventful api doesn't really have data for things like "going" or "num_watching" or anything to indicate how many people are attending
		- It does have a "popularity" rating which can be useful, we need to look more into other features we can use