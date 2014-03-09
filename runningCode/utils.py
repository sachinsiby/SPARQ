#Author- Sachin Siby
from SimpleCV import Image,Color
import colorsys
import sys


def chargingStationLocation(maxX,maxY,centroidX,centroidY):

	#top left
	if centroidX <= (1/3.0)*maxX and centroidY <= (1/3.0)*maxY:
		#return 'top left'
		sys.stderr.write("0")
		return 0
	#top
	elif centroidX <= (2/3.0)*maxX and centroidY <= (1/3.0)*maxY:
		#return 'top'
		return 4

	#top right
	elif centroidX <= maxX and centroidY <= (1/3.0)*maxY:
		#return 'top right'
		sys.stderr.write("1")
		return 2

	#middle left
	elif centroidX <= (1/3.0)*maxX and centroidY <= (2/3.0)*maxY:
		#return 'middle left'
		return 0

	#middle
	elif centroidX <= (2/3.0)*maxX and centroidY <= (2/3.0)*maxY:
		#return 'middle'
		return 1

	#middle right
	elif centroidX <= maxX and centroidY <= (2/3.0)*maxY:
		#return 'middle right'
		return 2

	#bottom left
	elif centroidX <= (1/3.0)*maxX and centroidY <= maxY:
		#return 'bottom left'
		sys.stderr.write("0")
		return 0

	#bottom
	elif centroidX <= (2/3.0)*maxX and centroidY <= maxY:
		#return 'bottom'
		return 5

	#bottom right
	elif centroidX <= maxX and centroidY <= maxY:
		#return 'bottom right'
		sys.stderr.write("1")
		return 2

	else:
		return -1


#Removes all colors from image except blue
def onlyBlueColor(original):

	blue_original = original.colorDistance((3,28,48))
	only_station = (original - blue_original) * 9
	only_station.save("image_blue.png")
	return only_station

# Iterates through all 'blue blobs' and finds the 'bluedest' blob
# Does this by converting all values to HSV space and getting lowest Hue (closest to 0)
# Added change - converts all values to HSV and gets lowest value to Blue Hue
# TODO: change logic if many blue blobs in an image etc
def chooseBestBlob(blobs):
	
	currBlueMin = 100
	#blueHue = 208 #180 degrees is lowest blue value 
	blueHue = 50
	maxArea = 0
	for blob in blobs:
 		blobMean = colorsys.rgb_to_hsv(blob.meanColor()[0],blob.meanColor()[1],blob.meanColor()[2])
		blob.drawMinRect(color=Color.YELLOW)
		checkValue = blobMean[0]*100 - blueHue 
		if blob.area() > maxArea:
			currBlueMin = checkValue
			station_blob = blob
			maxArea = blob.area()
	
	return station_blob

def detectChargingStation(image_file):
	
	original = Image(image_file)

	only_station = onlyBlueColor(original)

	blobs = only_station.findBlobs(threshval=(0,0,160),minsize=1000)
	blobs.image = original

	station_blob = chooseBestBlob(blobs)
	station_blob.drawMinRect(color=Color.RED)

	only_station.save("station_blob.png")
	original.save("modified_hair.png")

	centroidX = station_blob.minRectX()
	centroidY = station_blob.minRectY()

	#Have to find out which part of the screen centroid is in
	maxX = original.getNumpy().shape[0]
	maxY = original.getNumpy().shape[1]

	#print "Coordinates of centroid are "+str(centroidX)+", "+str(centroidY)
	#print "Coordinates of max are "+str(maxX)+", "+str(maxY)

	return chargingStationLocation(maxX,maxY,centroidX,centroidY)



def main():
	returnValue = detectChargingStation('image.png')
	print returnValue
	
if __name__ == '__main__':
	main()
