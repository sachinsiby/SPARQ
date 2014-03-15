#Author- Sachin Siby
from SimpleCV import Image,Color
import colorsys
import sys
from math import sqrt
from itertools import izip
import os

globCounter = 0


def cosine_measure(v1, v2):
    return (lambda (x, y, z): x / sqrt(y * z))(reduce(lambda x, y: (x[0] + y[0] * y[1], x[1] + y[0]**2, x[2] + y[1]**2), izip(v1, v2), (0, 0, 0)))


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
		sys.stderr.write("0");
		return 0

	#middle
	elif centroidX <= (2/3.0)*maxX and centroidY <= (2/3.0)*maxY:
		#return 'middle'
		return 1

	#middle right
	elif centroidX <= maxX and centroidY <= (2/3.0)*maxY:
		#return 'middle right'
		sys.stderr.write("1");
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
		sys.stderr.write("-1");
		return -1


def chargingStationLocation_New(maxX, maxY,centroidX,centroidY,width):

	#Gets a width in pixels
	

	#Centre coordinates of the image
	imageCentreX = maxX/2
	imageCentreY = maxY/2

	#Calculates center block leftX and rightX
	centreBlockX1 = imageCentreX - width/2
	centreBlockX2 = imageCentreX + width/2



	if centroidY < (1/3.0)* maxY:
		yDirection = 'bottom'

	elif centroidY > (1/3.0)* maxY  and centroidY < (2/3.0)*maxY:
		yDirection = 'middle'

	elif centroidY > (2/3.0)*maxY:
		yDirection = 'top'


	#First preference to x axis movement
	if centroidX < centreBlockX1:
		xDirection = 'left'
		if yDirection == 'top':
			sys.stderr.write("0")
			return 0
		elif yDirection == 'middle':
			return 0
		elif yDirection == 'bottom':
			sys.stderr.write("0")
			return 0
		
	elif centroidX > centreBlockX1 and centroidX < centreBlockX2:
		xDirection ='center' #not Needed
		if yDirection == 'bottom':
			#moveDown
			return 5
		elif yDirection == 'middle':
			#moveStraight
			return 1
		elif yDirection == 'top':
			#moveUp
			return 4
		
	elif centroidX > centreBlockX2:
		xDirection = 'right'
		if yDirection == 'top':
			sys.stderr.write("0")
			return 2
		elif yDirection == 'middle':
			return 2
		elif yDirection == 'bottom':
			sys.stderr.write("1")
			return 2

	#print "xDirection is ", xDirection
	#print "yDirection is ", yDirection
	return 99

#Removes all colors from image except blue
def onlyBlueColor(original):

	blue_original = original.colorDistance((3,28,48))
	only_station = (original - blue_original) * 9
	#only_station.save("image_blue.png")
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


def chooseBestBlobCosine(blobs):

	maxSimilarity = 0
	compareTuple = (0,19,54)

	for blob in blobs:
		meanColorTuple = (blob.meanColor()[0],blob.meanColor()[1],blob.meanColor()[2])
		blob.drawMinRect(color=Color.YELLOW)
		if cosine_measure(meanColorTuple,compareTuple) > maxSimilarity:
			maxSimilarity = cosine_measure(meanColorTuple,compareTuple)
			#print meanColorTuple," ",cosine_measure(meanColorTuple,compareTuple)
			station_blob = blob

	return station_blob

def detectChargingStation(image_file):
	
	global globCounter

	globCounter= globCounter+1
	original = Image(image_file)

	only_station = onlyBlueColor(original)

	#blobs = only_station.findBlobs(threshval=(0,0,160),minsize=1000)

	#Different findBlobs
	mask = original.binarize().dilate(2)
	blobs = only_station.findBlobsFromMask(mask)

	#print "Number of blobs found" , len(blobs)
	blobs.image = original

	station_blob = chooseBestBlobCosine(blobs)
	station_blob.drawMinRect(color=Color.RED)

	#only_station.save("station_blob.png")
	#original.save("modified_hair.png")
	original.save("finding_blob_"+str(globCounter)+".png")

	centroidX = station_blob.minRectX()
	centroidY = station_blob.minRectY()

	#Have to find out which part of the screen centroid is in
	maxX = original.getNumpy().shape[0]
	maxY = original.getNumpy().shape[1]

	#print "Coordinates of centroid are "+str(centroidX)+", "+str(centroidY)
	#print "Coordinates of max are "+str(maxX)+", "+str(maxY)

	#return chargingStationLocation(maxX,maxY,centroidX,centroidY)

	#Width is 100 pixels
	return chargingStationLocation_New(maxX,maxY,centroidX,centroidY,200)


def main():

	returnValue = detectChargingStation('image.png')
	print returnValue

if __name__ == '__main__':
	main()
