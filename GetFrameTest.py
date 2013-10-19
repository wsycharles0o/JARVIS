from cv2 import cv
from GetFrame import init,camara_available,get_point,get_capture,get_time,get_image,get_thresholded_image,calculate_point,get_frame
def test():
    init()
    if not camara_available(): print "dead"; return
    while(True):
        l = get_frame( [ (cv.Scalar(90,160,60),cv.Scalar(120,256,256)) ] )
        print "{0}".format(l)
     
def test_efficiency():
    #cv.NamedWindow("th");
    #cv.NamedWindow("v");
    capture = get_capture();
    init_delay_counter = 0
    prevtime = get_time()
    prevtimestamp = prevtime
    count = 0
    l = [0 ,0, 0, 0,0]
    while True:
        t = get_time()        
        frame, timestamp = get_image(capture)
        #print "-------------get_frame: {0}".format(t-prevtime)
        l[0] += t-prevtime
        prevtime = t
        
        #t = get_time()
        #frame = blur_frame(frame)
        #print "blur_frame: {0}".format(t-prevtime)
        #l[1] += t-prevtime
        #prevtime = t
        
        if frame is None: 
            init_delay_counter+=1
            if init_delay_counter > 10: break;
            continue
        
        t = get_time()
        img_threshed = get_thresholded_image(frame, cv.Scalar(90,160,60),cv.Scalar(120,256,256))
        #print "get_thresholded_image: {0}".format(t-prevtime)
        l[2] += t-prevtime
        prevtime = t
        
        t = get_time()
        x, y, area = calculate_point(img_threshed)
        #print "get_point: {0}".format(get_time()-prevtime)
        l[3] += t-prevtime
        prevtime = t
        
        #print "Result: ({0}, {1}, {2}) @ {3} : {4} secs".format(x, y, area, timestamp, timestamp - prevtimestamp)
        l[4] += timestamp - prevtimestamp
        prevtimestamp = timestamp
        count+=1
        if count > 100: break
        #print frame[320,240]
        #cv.ShowImage("v", frame)
        #cv.ShowImage("th",img_threshed)
        #c = cv.WaitKey(10)
        #if c is not -1: break
    print "get_frame: {0}".format(l[0]/count)
    print "blur_frame: {0}".format(l[1]/count)
    print "get_thresholded_image: {0}".format(l[2]/count)
    print "get_point: {0}".format(l[3]/count)
    print "all: {0}".format(l[4]/count)
    
test()