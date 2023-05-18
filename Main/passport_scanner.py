"""
==========================================
Python Passport Scanner
==========================================

Description: Passport scanner module that transcribes Machine Readable Zone of the passport into JSON
Language: Python 3.9.4
-------------------------------------------------------------
"""

import cv2
import time
import json
from time import sleep as nap
from passporteye import read_mrz


def scan():
    """
    Scans a passport document. Reads and transcribes the machine Readable Zone in the
    passport. Recognizes a passport through identifying the face in the passport

    returns:
    -------

    mrz_json: JSON, json object containing scanned passport information
    """
        
    # Load cascade
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml') # loading face recognition

    # define video stream source
   
    cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)

    counter = 0 # for counting frames

    process_this_frame = True
    delay = 5
    start_time = time.time()
    cv2.namedWindow("initial")

    while time.time() - start_time < delay:
        ret, frame = cap.read()
        cv2.imshow('initial', frame)
        cv2.waitKey(1)

    cv2.destroyWindow('initial')
    while True:
        
        #while time.time() - start_time < 0.5: # half second delay between each scan
            #ret, frame = cap.read()
            #cv2.imshow('Camera Stream', frame)
            #cv2.waitKey(1)
        
        # Read the frame
        _, img = cap.read()
        
        # Convert to grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # Detect the faces with grayscale
        faces = face_cascade.detectMultiScale(gray, 1.1, 4)

        for (x, y, w, h) in faces:
            
            cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)

            if counter == 13: # create a delay of 13 frames till picture is taken
                counter -= 13
                cv2.imwrite("passport.jpg", img)
                nap(1)
                mrz = read_mrz("passport.jpg")
                
                try:
                    
                    mrz_data = mrz.to_dict() # convert field-value to dictionary tuple
                    mrz_json = json.dumps(mrz_data, indent = 4) # convert to json
                    mrz_json = json.loads(mrz_json) # additional formatting required
                    
                    if mrz_json["valid_score"] != 100: # only a clear passport will be considered
                        print("continue scanning...")

                    else:
                        print(mrz_json)
                        return mrz_json
                        cv2.destroyAllWindows()

                    
                except AttributeError:
                    print("Scanning...")
                    
        #process_this_frame = not process_this_frame # skip next frame
                
            counter += 1  
        # Display
        cv2.imshow('Stream', img)
        
        # Stop if escape key is pressed
        k = cv2.waitKey(30) & 0xff
        if k==27:
            break
        
    # Release VideoCapture object
    cap.release()
