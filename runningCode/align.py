from SimpleCV import Image,Color, DrawingLayer
from itertools import izip
from math import sqrt

def cosine_measure(v1, v2):
    return (lambda (x, y, z): x / sqrt(y * z))(reduce(lambda x, y: (x[0] + y[0] * y[1], x[1] + y[0]**2, x[2] + y[1]**2), izip(v1, v2), (0, 0, 0)))


def detectGreenLowQuality(image_file):
	
	original = Image(image_file)

	#binarizedYellowMask = findYellowMask(image_file)
	#subtractedMask = original - binarizedYellowMask
	#subtractedMask.save("subtractedMask.jpg")

	#green_only = subtractedMask.colorDistance((94,116,33))
	#green_only = subtractedMask.colorDistance((50,116,45))
	green_only = original.colorDistance((0,70,6))

	green_only = green_only*6

	mask = green_only.invert()
	#mask.save("green_mask.jpg")


	binarizedMask = mask.binarize().invert()
	#binarizedMask.save("binarized_mask_green.jpg")


	blobs = original.findBlobsFromMask(binarizedMask)


	if blobs == None:
		#print "No green found"
		return detectYellowLowQuality(image_file)


	blobs.image = original
	
	#Assume best blob is the largest blob
	bestBlob = blobs[-1]

	bestBlob.drawMinRect(color=Color.RED,width =10)
	#original.save("foundBlobs_green.jpg")
	

	'''
	#blobs[-1].drawRect(color=Color.RED,width =10)
	coordinates = bestBlob.minRect()


	#Find the center point
	centroidX = bestBlob.minRectX()
	centroidY = bestBlob.minRectY()

	minLeftY = 0
	minRightY = 0

	#Find the bottom left and bottom right coordinates
	for coordinate in coordinates:
		if coordinate[0] < centroidX and coordinate[1] > minLeftY:
			bottomLeft = coordinate
			minLeftY = coordinate[1]
		elif coordinate[0] > centroidX and coordinate[1] > minRightY:
			bottomRight = coordinate
			minRightY = coordinate[1]
			
	'''


	centroidX = bestBlob.minRectX()
	centroidY = bestBlob.minRectY()

	#Have to find out which part of the screen centroid is in
	maxX = original.getNumpy().shape[0]
	maxY = original.getNumpy().shape[1]+100
	

	#assume width of 150 pixels
	return align_center(maxX,maxY,centroidX,centroidY,50,50)



def detectYellowLowQuality(image_file):

	original = Image(image_file)

	yellow_only = original.colorDistance((156,130,76))*2
	#yellow_only = yellow_only*4

	mask = yellow_only.invert()
	#mask.save("yellow_mask.jpg")

	binarizedMask = mask.binarize().invert()
	#binarizedMask.save("binarized_mask_yellow.jpg")

	blobs = original.findBlobsFromMask(binarizedMask)

	if blobs == None:
		#print "No yellow found"
		return -1

	blobs[-1].drawMinRect(color=Color.RED,width =10)
	blobs.image = original

	#original.save("foundBlobs_yellow.jpg")

	bestBlob = blobs[-1]


	centroidX = bestBlob.minRectX()
	centroidY = bestBlob.minRectY()

	#Have to find out which part of the screen centroid is in
	maxX = original.getNumpy().shape[0]
	maxY = original.getNumpy().shape[1]+100
	

	#assume width of 150 pixels
	return align_center(maxX,maxY,centroidX,centroidY,50,50)

def detectCenter(image_file):

	original = Image(image_file)

	center_only = original.colorDistance((155,9,49))*8

	mask = center_only.invert()
	#mask.save("center_mask.jpg")

	binarizedMask = mask.binarize().invert()
	#binarizedMask.save("binarized_mask_center.jpg")

	blobs = original.findBlobsFromMask(binarizedMask)

	if blobs == None :
		#print "No red found"
		return detectGreenLowQuality(image_file)


	bestBlob = blobs[-1]
	bestBlob.drawMinRect(color=Color.RED,width =10)

	bestBlob.image = original

	original.save("align.png")


	centroidX = bestBlob.minRectX()
	centroidY = bestBlob.minRectY()

	#Have to find out which part of the screen centroid is in
	maxX = original.getNumpy().shape[0]
	maxY = original.getNumpy().shape[1]+100
	

	#assume width of 150 pixels
	return align_center(maxX,maxY,centroidX,centroidY,80,80)

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

def isCenterAndUp(reference,position):
	if position < reference:
		return True
	return False

def isCenterAndDown(reference,position):
	if position > reference:
		return True
	return False

def align_center(maxX, maxY,centroidX,centroidY,widthX, widthY):

	imageCenterX = maxX/2
	imageCenterY = maxY/2 - 50

	centerBlockX1 = imageCenterX - widthX/2 #Left
	centerBlockX2 = imageCenterX + widthX/2 #Right


	centerBlockY1 = imageCenterY + widthY/2 #Lower
	centerBlockY2 = imageCenterY - widthY/2 #Upper

	if(isLeft(centerBlockX1, centroidX)):
			return 3
	if(isRight(centerBlockX2, centroidX)):
			return 4

	if(isCenterBlock(centerBlockX1, centerBlockX2, centroidX)):
		if(isCenterAndDown(centerBlockY1,centroidY)):
			#move backward
			return 5
		if(isCenterAndUp(centerBlockY2,centroidY)):
			#move forward
			return 2
		return 6

	return 99

def detectBlobs(image_file):
	
	original = Image(image_file)
	blobs = original.findBlobs()
	
	for blob in blobs:
		blob.drawMinRect(color=Color.RED,width =10)

	#blobs[-1].drawMinRect(color=Color.RED,width =10)
	blobs.image = original
	#original.save("foundBlobs.jpg")
	return 1

def findYellowMask(image_file):
	original = Image(image_file)

	yellow_only = original.colorDistance((232,166,30))
	yellow_only = yellow_only*4

	mask = yellow_only.invert()
	#mask.save("yellow_mask.jpg")

	binarizedMask = mask.binarize().invert()
	#binarizedMask.save("binarized_mask_yellow.jpg")

	return binarizedMask


def startProcessing():
	pass



def main():
	#returnValue = detectLandingPads('landing4.jpg')
	#returnValue = detectGreenLowQuality('image113_1.png')
	#returnValue = detectYellowLowQuality('image113_1.png')
	#returnValue = detectBlobs('image113_1.png')
	returnValue = detectCenter('image.png')
	print returnValue


if __name__ == '__main__':
	main()
