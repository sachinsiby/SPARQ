from SimpleCV import Image,Color, DrawingLayer
from itertools import izip
from math import sqrt

def cosine_measure(v1, v2):
    return (lambda (x, y, z): x / sqrt(y * z))(reduce(lambda x, y: (x[0] + y[0] * y[1], x[1] + y[0]**2, x[2] + y[1]**2), izip(v1, v2), (0, 0, 0)))


def detectGreenLowQuality(image_file):
	
	original = Image(image_file)

	binarizedYellowMask = findYellowMask(image_file)
	subtractedMask = original - binarizedYellowMask
	subtractedMask.save("subtractedMask.jpg")

	#green_only = subtractedMask.colorDistance((94,116,33))
	#green_only = subtractedMask.colorDistance((50,116,45))
	green_only = subtractedMask.colorDistance((0,70,6))

	green_only = green_only*5

	mask = green_only.invert()
	mask.save("green_mask.jpg")


	binarizedMask = mask.binarize().invert()
	binarizedMask.save("binarized_mask_green.jpg")


	blobs = original.findBlobsFromMask(binarizedMask)


	if len(blobs) == 0:
		return -1


	print"Length of blobs is ", len(blobs)
	blobs.image = original
	

	#Assume best blob is the largest blob
	bestBlob = blobs[-1]

	bestBlob.drawMinRect(color=Color.RED,width =10)
	
	#blobs[-1].drawRect(color=Color.RED,width =10)
	coordinates = bestBlob.minRect()
	print "Coordinates of the rect are ", str(coordinates)
	print"##################################"


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
			
	print "Bottom left coordinate- ", str(bottomLeft)
	print "Bottom right coordinate- ", str(bottomRight)
	

	if bottomLeft[1] < bottomRight[1]:
		print "Rotate counter clockwise "
	else:
		print "Rotate clockwise"


	original.save("foundBlobs_green.jpg")
	return 1

def detectYellowLowQuality(image_file):

	original = Image(image_file)

	yellow_only = original.colorDistance((156,130,76))*2
	#yellow_only = yellow_only*4

	mask = yellow_only.invert()
	mask.save("yellow_mask.jpg")

	binarizedMask = mask.binarize().invert()
	binarizedMask.save("binarized_mask_yellow.jpg")

	blobs = original.findBlobsFromMask(binarizedMask)

	if len(blobs) == 0 :
		return -1

	'''
	for blob in blobs:
		blob.drawMinRect(color=Color.RED,width =10)

	'''
	blobs[-1].drawMinRect(color=Color.RED,width =10)
	blobs.image = original
	original.save("foundBlobs_yellow.jpg")

	return 1

def detectCenter(image_file):

	original = Image(image_file)

	center_only = original.colorDistance((155,9,49))*2
	#yellow_only = yellow_only*4

	mask = center_only.invert()
	mask.save("center_mask.jpg")

	binarizedMask = mask.binarize().invert()
	binarizedMask.save("binarized_mask_center.jpg")

	blobs = original.findBlobsFromMask(binarizedMask)

	if len(blobs) == 0 :
		return -1


	bestBlob = blobs[-1]
	bestBlob.drawMinRect(color=Color.RED,width =10)


	centroidX = bestBlob.minRectX()
	centroidY = bestBlob.minRectY()

	#Have to find out which part of the screen centroid is in
	maxX = original.getNumpy().shape[0]
	maxY = original.getNumpy().shape[1]+100
	

	#assume width of 150 pixels
	return align_center(maxX,maxY,centroidX,centroidY,150,80)

	'''
	blobs.image = original
	original.save("foundBlobs_center.jpg")
	return 1
	'''

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
	imageCenterY = maxY/2

	centerBlockX1 = imageCenterX - widthX/2 #Left
	centerBlockX2 = imageCenterX + widthX/2 #Right


	centerBlockY1 = imageCenterY + widthY/2 #Lower
	centerBlockY2 = imageCenterY - widthY/2 #Upper


	if(isLeft(centerBlockX1, centroidX)):
			print "Left"
			return 3
	if(isRight(centerBlockX2, centroidX)):
			print "Right"
			return 4
	if(isCenterBlock(centerBlockX1, centerBlockX2, centroidX)):
			if(isCenterAndDown(centerBlockY1,centroidY)):
				#move backward
				print "Down"
				return 5
			if(isCenterAndUp(centerBlockY2,centroidY)):
				#move forward
				print "Up"
				return 2
			else:
				return 6
	return 99

def detectBlobs(image_file):
	
	original = Image(image_file)
	blobs = original.findBlobs()
	
	for blob in blobs:
		blob.drawMinRect(color=Color.RED,width =10)

	#blobs[-1].drawMinRect(color=Color.RED,width =10)
	blobs.image = original
	original.save("foundBlobs.jpg")
	return 1

def findYellowMask(image_file):
	original = Image(image_file)

	yellow_only = original.colorDistance((232,166,30))
	yellow_only = yellow_only*4

	mask = yellow_only.invert()
	mask.save("yellow_mask.jpg")

	binarizedMask = mask.binarize().invert()
	binarizedMask.save("binarized_mask_yellow.jpg")

	return binarizedMask


def startProcessing():
	pass



def main():
	#returnValue = detectLandingPads('landing4.jpg')
	#returnValue = detectGreenLowQuality('image113_1.png')
	#returnValue = detectYellowLowQuality('image113_1.png')
	#returnValue = detectBlobs('image113_1.png')
	returnValue = detectCenter('image164.png')
	print returnValue


if __name__ == '__main__':
	main()