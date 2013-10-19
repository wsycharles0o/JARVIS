from cv2 import cv

def get_capture():
    """
    Starts capturing from camera. If cannot init capturing, return None.
    """
    capture = cv.CaptureFromCAM(0);
    if not capture:
        print "Could not init capturing."
        return None
    return capture

def get_frame(capture):
    """
    Start grabbing a frame. If can't grab a frame, return None.
    """
    frame = cv.QueryFrame(capture);
    if not frame:
        return None
    return frame

def get_thresholded_image(frame, range1, range2):
    """
    range1, range2: init by cv.Scalar(h, s, v)
    """
    img_hsv = cv.CreateImage(cv.GetSize(frame), 8, 3);
    cvCvtColor(frame, img_hsv, CV_BGR2HSV);
    img_threshed = cvCreateImage(cvGetSize(frame), 8, 1);
    cv.InRangeS(img_hsv, range1, range2, img_threshed);
    return img_threshed
  
    
