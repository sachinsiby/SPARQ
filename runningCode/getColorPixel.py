from SimpleCV import Image

x = Image("image_blue.png")
y = x.getNumpy()
print y[341][208];
