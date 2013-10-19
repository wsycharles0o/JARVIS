from cv2 import cv


def GetThresholdedImage(img):
    imgHSV = cv.CreateImage(cv.GetSize(img), 8, 3)
    #imgRGB = cv.CreateImage(cv.GetSize(img), 8, 3)
    #cv.Smooth(img,img,cv.CV_GAUSSIAN,3,3)
    cv.CvtColor(img, imgHSV, cv.CV_BGR2HSV)
    #cv.CvtColor(img, imgRGB, cv.CV_BGR2RGB)
    #imgHSV = img
    # print imgHSV[320,240] #DEBUG
    imgThreshed = cv.CreateImage(cv.GetSize(img), 8, 1)
    #cv.InRangeS(imgRGB, ,cv.Scalar(,0,255) ,cv.Scalar(120,0,255) ,imgThreshed)
    cv.InRangeS(imgHSV, cv.Scalar(90,160,60),cv.Scalar(120,256,256), imgThreshed) # yellowish
    #cv.InRangeS(img, cv.Scalar(20, 100, 100),cv.Scalar(40,40,255), imgThreshed) # yellowish
    cv.Smooth(imgThreshed, imgThreshed, cv.CV_GAUSSIAN, 3, 3)
    return imgThreshed

# main
def __main__():
    capture = cv.CaptureFromCAM(0)
    if not capture:
            print "CAN'T INIT CAPTURING..."
            sys.exit(-1)
    cv.NamedWindow("video")
    cv.NamedWindow("th")
    #imgScribble = None
    counter = 1
    while True:
            frame = cv.QueryFrame(capture)
            if not frame:
                    counter += 1
                    if counter>10: break # only wait 10 loops
                    continue
            #if imgScribble is not None:
            #        imgScribble = cv.CreateImage(cv.GetSize(frame), 8, 3)
            imgYellowThresh = GetThresholdedImage(frame)
            print type(imgYellowThresh)
            #moments = cv.Moments(imgYellowThresh, 1) # FIXME
            #moment10 = cv.GetSpatialMoment(moments,1,0)
            #moment01 = cv.GetSpatialMoment(moments,0,1)
            #area = cv.GetCentralMoment(moments,0,0)
            #posX = 0
            #poxY = 0
            #lastX = posX
            #lastY = posY
            #posX = moment10/area
            #posY = moment01/area
            #print "position {0},{1}".format(posX,posY)
            #if imgScribble is not None:
            #        cv.Add(frame, imgScribble, frame)
            cv.ShowImage("th", imgYellowThresh)
            cv.ShowImage("video", frame);
            c = cv.WaitKey(10)
            if c is not -1: break
__main__()
