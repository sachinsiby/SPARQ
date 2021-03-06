#Author- Sachin Siby
#FIxed by Zerzar
from SimpleCV import Image,Color, DrawingLayer
import colorsys
import sys
from math import sqrt
from itertools import izip
import os

globCounter = 0


def cosine_measure(v1, v2):
    return (lambda (x, y, z): x / sqrt(y * z))(reduce(lambda x, y: (x[0] + y[0] * y[1], x[1] + y[0]**2, x[2] + y[1]**2), izip(v1, v2), (0, 0, 0)))



def isLeft(reference, position):
	if(position < reference):
		return True
	return False

def isRight(reference, position):
	if(position > reference):
		return True
	return False

def isCenterBlock(blockLeft, blockRight, position):
	if(position > blockLeft and position < blockRight):
		return True
	return False



def chargingStationLocation_New(maxX, maxY,centroidX,centroidY,width, ratio, blobArea):

	goldenRatio = 137/145.0

	sys.stderr.write(str(abs(goldenRatio-ratio)))

	#Gets a width in pixels
	

	#Center coordinates of the image
	imageCenterX = maxX/2
	imageCenterY = maxY/2

	#Calculates center block leftX and rightX
	centerBlockX1 = imageCenterX - width/2
	centerBlockX2 = imageCenterX + width/2


	if(abs(ratio - goldenRatio) > 0.21 and blobArea < 60000):
		if(isRight(centerBlockX1, centroidX)):
			return 0
		if(isLeft(centerBlockX2, centroidX)):
			return 1
		if(isCenterBlock(centerBlockX1, centerBlockX2, centroidX)):
			return 2
	else:
		if(isLeft(centerBlockX1, centroidX)):
			return 3
		if(isRight(centerBlockX2, centroidX)):
			return 4
		if(isCenterBlock(centerBlockX1, centerBlockX2, centroidX)):
			return 5

	return 99

#Removes all colors from image except blue
def onlyBlueColor(original, colorPick):

	blue_original = original.colorDistance(colorPick)
	only_station = (original - blue_original) * 0.5
	return only_station

def chooseBestBlobCosine(blobs):

	maxSimilarity = 0
	compareTuple = (8,33,64)

	for blob in blobs:
		meanColorTuple = (blob.meanColor()[0],blob.meanColor()[1],blob.meanColor()[2])
		blob.drawMinRect(color=Color.YELLOW)
		if cosine_measure(meanColorTuple,compareTuple) > maxSimilarity:
			maxSimilarity = cosine_measure(meanColorTuple,compareTuple)
			#print meanColorTuple," ",cosine_measure(meanColorTuple,compareTuple)
			station_blob = blob

	return station_blob

def isWhite(img):
	x = img.meanColor()
	for i in range(0,2):
		if(x[i] != 255):
			return False
	return True

def detectChargingStation(image_file):
	debug = False

	myColor1 = (8,33,64)
	myColor2 = (70,80,100)

	original = Image(image_file)

	only_station = onlyBlueColor(original, myColor1)

	#Different findBlobs
	maskMean = original.hueDistance(color=(200,160,150))
	mask = only_station.hueDistance(color=myColor1).binarize()
	meanColor = (round(((maskMean.meanColor()[0]+maskMean.meanColor()[1]+maskMean.meanColor()[2])/3) * 10000)/10000)
	blobs = original.findBlobsFromMask(mask, minsize=400)

	if(meanColor > 190):
		return 6

	#print "Number of blobs found" , len(blobs)
	try: 
		blobs.image = original
	except Exception:
		only_station = onlyBlueColor(original, myColor2)
		mask = only_station.hueDistance(color=myColor2).binarize()
		blobs = original.findBlobsFromMask(mask, minsize=400)
		blobs.image = original

	station_blob = chooseBestBlobCosine(blobs)
	station_blob.drawMinRect(color=Color.RED)

	centroidX = station_blob.minRectX()
	centroidY = station_blob.minRectY()

	#Have to find out which part of the screen centroid is in
	maxX = original.getNumpy().shape[0]
	maxY = original.getNumpy().shape[1]+100

	if(debug):
		centroidLayer = DrawingLayer((maxX,maxY))

		centroidLayer.line((0,(1/3.0)*maxY),(maxX, (1/3.0)*maxY), color=Color.GREEN, width=2)
		centroidLayer.line((0,(2/3.0)*maxY),(maxX, (2/3.0)*maxY), color=Color.GREEN, width=2)
		centroidLayer.circle((int(centroidX), int(centroidY)), color=Color.GREEN, radius=5, filled=True)

		original.addDrawingLayer(centroidLayer)
		original.applyLayers()

		mask.save("binarizeMask.png")
		original.save("blobs.png")
		only_station.save("blueFilter.png")

	#print "Coordinates of centroid are "+str(centroidX)+", "+str(centroidY)
	#print "Coordinates of max are "+str(maxX)+", "+str(maxY)

	#if(station_blob.width() * station_blob.height() < 4000):
	#	return 2

	blobArea = station_blob.width() * station_blob.height()

	if(blobArea < 10000):
		return 2

	return chargingStationLocation_New(maxX,maxY,centroidX,centroidY,200, station_blob.width() / float(station_blob.height()), blobArea)


def main():

	img = "image.png"

	if(len(sys.argv) > 1):
		img = "/Users/z/copterImages/image" + sys.argv[1] + ".png"

	returnValue = detectChargingStation(img)
	print returnValue

if __name__ == '__main__':
	main()
