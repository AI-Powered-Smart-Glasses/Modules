import cv2
import sys

# sys.path.append('Module-1')
# from voice import *

# sys.path.append('Module-2')
# from OCR import *

# sys.path.append('Module-3')
# from Image_Captioning import *

# sys.path.append('Module-4')
# from reco import *

# sys.path.append('Module-5')
# from classification import *

# sys.path.append('Module-6')
# from traffic_light import *

def reco():
    count = "randomString"
    cap = cv2.VideoCapture(0)
    counter=0
    
    print("Capturing Frame")
    ret, frame = cap.read()
    nm="NewFrame/frame"+str(count)+".jpg"
    print("Frame Captured")
    cv2.imwrite(nm, frame)
    # recognise(nm)

def caption():
    count = "randomString"
    cap = cv2.VideoCapture(0)
    counter=0
    
    print("Capturing Frame")
    ret, frame = cap.read()
    nm="NewFrame/frame"+str(count)+".jpg"
    print("Frame Captured")
    cv2.imwrite(nm, frame)
    # voice(caption_this_image(nm))

def doclassify():
    count = "randomString"
    cap = cv2.VideoCapture(0)
    counter=0
    
    print("Capturing Frame")
    ret, frame = cap.read()
    nm="NewFrame/frame"+str(count)+".jpg"
    print("Frame Captured")
    cv2.imwrite(nm, frame)
    # voice(classify(nm))

def trafficLights():
    count = "randomString"
    cap = cv2.VideoCapture(0)
    counter=0
    
    print("Capturing Frame")
    ret, frame = cap.read()
    nm="NewFrame/frame"+str(count)+".jpg"
    print("Frame Captured")
    cv2.imwrite(nm, frame)
    # traffic_lig(nm)

def ocrImage():
    count = "randomString"
    cap = cv2.VideoCapture(0)
    counter=0
    
    print("Capturing Frame")
    ret, frame = cap.read()
    nm="NewFrame/frame"+str(count)+".jpg"
    print("Frame Captured")
    cv2.imwrite(nm, frame)
    # ocr(nm)
