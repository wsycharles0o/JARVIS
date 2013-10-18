from cv2 import cv


def GetThresholdedImage(img):
    imgHSV = cv.CreateImage(cv.GetSize(img), 8, 3)
    cv.CvtColor(img, imgHSV, cv.CV_BGR2HSV)
    imgThreshed = cv.CreateImage(cv.GetSize(img), 8, 1)
    cv.InRangeS(imgHSV, cv.Scalar(20,100,100),cv.Scalar(30,255,255), imgThreshed) # yellowish
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
while True:
    frame = cv.QueryFrame(capture)
    if not frame: break
    if imgScribble is not None:
        imgScribble = cv.CreateImage(cv.GetSize(frame), 8, 3)
    imgYellowThresh = GetThresholdedImage(frame)
    # cv.Add(frame, imgScribble, frame)
    cv.ShowImage("th", imgYellowThresh)
    cv.ShowImage("video", frame);
    c = cv.WaitKey(10)
    if c is not -1: break
