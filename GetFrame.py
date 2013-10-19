__author__="Jacky"
__date__ ="$Oct 18, 2013 6:44:33 PM$"

from cv2 import cv
import time

AREA_THRESHOLD = 5000.0 # smaller than this: regard as 0.
capture = None
_debug = False
_color_names = []
CAMERA_WINDOW = "Camera"

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

def get_image(capture):
    """
    Return (frame, time)
    Start grabbing a image from camera. If can't grab a frame, frame is None.
    time: time of capturing.
    """
    frame = cv.QueryFrame(capture);
    #frame = blur_frame(frame) # TURN OFF BLURRING HERE
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
    mat = img_threshed[:,:]
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

def get_point(frame, range1, range2, color_num):
    img_threshed = get_thresholded_image(frame, range1,range2)
    if _debug: cv.ShowImage(_color_names[color_num], img_threshed)
    x, y, area = calculate_point(img_threshed)
    return (x, y, area)

#Available outside

def init(debug = False, color_names = []):
    global capture
    global _debug
    global _color_names
    capture = get_capture();
    _debug = debug
    _color_names = color_names
    if _debug:
        cv.NamedWindow(CAMERA_WINDOW)
        for color in _color_names:
            cv.NamedWindow(color)

def camara_available():
    """
    After init(), this predicate should be checked; if false, program should exit.
    """
    return capture is not None

def get_frame(ranges):
    """
    range1, range2: init by cv.Scalar(h, s, v)
    Return a list:
    the first element is the time stamp when image is captured
    the rest are three number tuples: (x, y, area, timestamp)
    x: None if object is not found, else object's mid point's x
    y: None if object is not found, else object's mid point's y
    area: 0 if object is not found, else object's area
        area only != 0  if it is calculated to be greater than AREA_THRESHOLD
    """
    if capture:
        frame, timestamp = get_image(capture)
        if _debug: cv.ShowImage(CAMERA_WINDOW, frame)
        result = [timestamp]
        i = 0
        for (range1, range2) in ranges:
            result.append(get_point(frame, range1, range2, i))
            i += 1
        if _debug: cv.WaitKey(10);
        return result
    return [get_time()] + [None] * len(ranges)
