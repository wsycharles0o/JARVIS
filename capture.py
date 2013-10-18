from cv2 import cv


def GetThresholdedImage(img):
	imgHSV = cv.CreateImage(cv.GetSize(img), 8, 3)
	cv.CvtColor(img, imgHSV, cv.CV_BGR2HSV)
	imgThreshed = cv.CreateImage(cv.GetSize(img), 8, 1)
	cv.InRangeS(imgHSV, cv.Scalar(90,100,100),cv.Scalar(120,240,240), imgThreshed) # yellowish
	#cv.ReleaseImage(imgHSV)
	return imgThreshed

# main
capture = cv.CaptureFromCAM(0)
if not capture:
	print "CAN'T INIT CAPTURING..."
	sys.exit(-1)
cv.NamedWindow("video")
cv.NamedWindow("th")
imgScribble = None
counter = 1
while True:
	frame = cv.QueryFrame(capture)
	if not frame:
		counter += 1
		if counter>10: break
		continue
	if imgScribble is not None:
		imgScribble = cv.CreateImage(cv.GetSize(frame), 8, 3)
	imgYellowThresh = GetThresholdedImage(frame)
	print imgYellowThresh
	moments = cv.Moments( imgYellowThresh ,1)
	moment10 = cv.GetSpatialMoment(moments,1,0)
	moment01 = cv.GetSpatialMoment(moments,0,1)
	area = cv.GetCentralMoment(moments,0,0)
	posX = 0
	poxY = 0
	lastX = posX
	lastY = posY
	posX = moment10/area
	posY = moment01/area
	print "position {0},{1}".format(posX,posY)
	if imgScribble is not None:
		cv.Add(frame, imgScribble, frame)
	cv.ShowImage("th", imgYellowThresh)
	cv.ShowImage("video", frame);
	c = cv.WaitKey(10)
	if c is not -1: break
