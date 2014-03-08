#Author- Sachin Siby
from SimpleCV import Image,Color
import colorsys



def chargingStationLocation(maxX,maxY,centroidX,centroidY):

	#top left
	if centroidX <= (1/3.0)*maxX and centroidY <= (1/3.0)*maxY:
		return 'top left'
	#top
	elif centroidX <= (2/3.0)*maxX and centroidY <= (1/3.0)*maxY:
		return 'top'

	#top right
	elif centroidX <= maxX and centroidY <= (1/3.0)*maxY:
		return 'top right'

	#middle left
	elif centroidX <= (1/3.0)*maxX and centroidY <= (2/3.0)*maxY:
		return 'middle left'

	#middle
	elif centroidX <= (2/3.0)*maxX and centroidY <= (2/3.0)*maxY:
		return 'middle'

	#middle right
	elif centroidX <= maxX and centroidY <= (2/3.0)*maxY:
		return 'middle right'

	#bottom left
	elif centroidX <= (1/3.0)*maxX and centroidY <= maxY:
		return 'bottom left'
	
	#bottom
	elif centroidX <= (2/3.0)*maxX and centroidY <= maxY:
		return 'bottom'

	#bottom right
	elif centroidX <= maxX and centroidY <= maxY:
		return 'bottom right'
	
	else:
		return 'no station'


#Removes all colors from image except red
def onlyRedColor(original):

	red_original = original.colorDistance(Color.RED)
	only_station = original - red_original
	return only_station

# Iterates through all 'red blobs' and finds the 'reddest' blob
# Does this by converting all values to HSV space and getting lowest Hue (closest to 0)
# TODO: change logic if many red blobs in an image etc
def chooseBestBlob(blobs):
	
	redMax = 360
	for blob in blobs:
		blobMean = colorsys.rgb_to_hsv(blob.meanColor()[0],blob.meanColor()[1],blob.meanColor()[2])
		#print "Hue is ",blobMean[0]*100
		#blob.drawMinRect(color=Color.YELLOW)
		if blobMean[0]*100 < redMax:
			redMax = blobMean[0]*100
			station_blob = blob

	return station_blob

def detectChargingStation(image_file):
	
	original = Image(image_file)

	only_station = onlyRedColor(original)
	mean_color_rgb = only_station.meanColor()
	

	blobs = only_station.findBlobs()
	blobs.image = original


	station_blob = chooseBestBlob(blobs)
	blobs.image = original
	station_blob.drawMinRect(color=Color.YELLOW)

	
	only_station.save("station_blob.png")
	original.save("modified_hair.png")

	centroidX = station_blob.minRectX()
	centroidY = station_blob.minRectY()

	#Have to find out which part of the screen centroid is in
	maxX = original.getNumpy().shape[0]
	maxY = original.getNumpy().shape[1]

	print "Coordinates of centroid are "+str(centroidX)+", "+str(centroidY)
	print "Coordinates of max are "+str(maxX)+", "+str(maxY)

	return chargingStationLocation(maxX,maxY,centroidX,centroidY)

def main():

	returnValue = detectChargingStation('hydrant5.jpg')
	print"Return is ",returnValue


if __name__ == '__main__':
	main()