__author__="Jacky"
__date__ ="$Oct 18, 2013 6:44:33 PM$"

from cv2 import cv
import numpy, time

AREA_THRESHOLD = 5000.0 # smaller than this: regard as 0.
capture = None

get_time = lambda: time.time()

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
    Return (frame, time)
    Start grabbing a frame. If can't grab a frame, frame is None.
    time: time of capturing.
    """
    frame = cv.QueryFrame(capture);
    t = get_time()
    return (frame,t)

def blur_frame(frame):
    """
    Return the blurred frame if it is not none.
    """
    if frame is not None:
        cv.Smooth(frame, frame, cv.CV_GAUSSIAN, 3, 3)
    return frame

def get_thresholded_image(frame, range1, range2):
    """
    range1, range2: init by cv.Scalar(h, s, v)
    """
    img_hsv = cv.CreateImage(cv.GetSize(frame), 8, 3);
    cv.CvtColor(frame, img_hsv, cv.CV_BGR2HSV);
    img_threshed = cv.CreateImage(cv.GetSize(frame), 8, 1);
    cv.InRangeS(img_hsv, range1, range2, img_threshed);
    return img_threshed

def calculate_point(img_threshed):
    """
    Return a three number tuple: (x, y, area)
    x: None if object is not found, else object's mid point's x
    y: None if object is not found, else object's mid point's y
    area: 0 if object is not found, else object's area
        area only != 0  if it is calculated to be greater than AREA_THRESHOLD
    """
    mat = cv.fromarray(numpy.asarray(img_threshed[:,:])) # FIXME very inefficient
    moments = cv.Moments(mat,0)
    moment10 = cv.GetSpatialMoment(moments, 1, 0);
    moment01 = cv.GetSpatialMoment(moments, 0, 1);
    area = cv.GetCentralMoment(moments, 0, 0);
    if area > AREA_THRESHOLD:
        x = moment10/area
        y = moment01/area
    else:
        x = None
        y = None
        area = None
    return (x, y, area)

def init():
    global capture
    capture = get_capture();

def camara_available():
    """
    After init(), this predicate should be checked; if false, program should exit.
    """
    return capture is not None

def get_point(range1, range2):
    """
    range1, range2: init by cv.Scalar(h, s, v)
    Return a three number tuple: (x, y, area, timestamp)
    x: None if object is not found, else object's mid point's x
    y: None if object is not found, else object's mid point's y
    area: 0 if object is not found, else object's area
        area only != 0  if it is calculated to be greater than AREA_THRESHOLD
    timestamp: timestamp when image is captured
    """
    if capture:
        frame, timestamp = get_frame(capture)
        img_threshed = get_thresholded_image(frame, range1,range2)
        x, y, area = calculate_point(img_threshed)
        return (x, y, area, timestamp)
    return (None, None, None, get_time())

