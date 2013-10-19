import cv2 as cv

def GetThresholdedImage(imgHSV):
	imgThresh = cv.CreateImage(cv.GetSize(imgHSV),IPL_DEPTH_8U,1)
	cv.InRangeS(imgHSV, cv.Scalar(170, 166, 60), cv.Scalar(180, 256, 256), imgThresh)
	return imgThresh

	cap = cv.VideoCapture(0)

	cv.namedWindow("Video")
	cv.namedWindow("Ball")
	while 1 is 1:
		frame = cap.read()
		if not frame:
                    break

	#frame = cv.CloneImage(frame)

	cv.GaussianBlur(frame, (3, 3), 0, frame)

	imgHSV = cv.CreateImage(cv.GetSize(frame), IPL_DEPTH_8U, 3)
	cv.CvtColor(frame, imgHSV, cv.CV_BGR2HSV)
	imgThresh = GetThresholdedImage(imgHSV)

	cv.GaussianBlur(frame, (3, 3), 0, frame)

	cv.ShowImage("Ball", imgThresh)
	cv.ShowImage("Video", frame)

	cv.ReleaseImage(imgHSV)
	cv.ReleaseImage(imgThresh)
	cv.ReleaseImage(frame)

	if cv.WaitKey(10) is 's':
		break

	cv.DestroyAllWindows()
	cv.ReleaseCapture(cap)
