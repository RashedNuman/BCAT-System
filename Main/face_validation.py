"""
==========================================
Fiducial Point Face Recognition 
==========================================

Description: Face recognition module which uses Fidcuial point algorithm to calculate similiarties
             between faces. requires 1 image as a dataset.
             
Language: Python 3.9.4
-------------------------------------------------------------
"""


import cv2
import base64
import numpy as np
import face_recognition


def face_verification(name):
    """
    Verifies passenger with the provided base64 encoding. Decodes base64
    back into an image, encodes it to a face encoding object and performs
    fudicial point detection to validate biometric identity.

    Note: Uses the 2nd video cam interface (1)

    Paramters
    ---------
    base64_img: str, base64 string representing the image on the passport

    returns
    -------
    boolean, true if faces match, false if they don't
    """

    #   1. Process each video frame at 1/4 resolution (though still display it at full resolution)
    #   2. Only detect faces in every other frame of video.


    passenger_image = face_recognition.load_image_file("passenger.jpg")
    passenger_face_encoding = face_recognition.face_encodings(passenger_image)[0] # encode face for processing
    
    # can be used to cross match with known fugitives
    # array of face encodings
    known_face_encodings = [passenger_face_encoding]
    
    # encoding match the names in index
    known_face_names = [name]


    face_locations = []
    face_encodings = []
    face_names = []
    process_this_frame = True
    counter = 0

    video_capture = cv2.VideoCapture(0, cv2.CAP_DSHOW)

    while True:
        # Grab a single frame of video
        ret, frame = video_capture.read()

        # Only process every other frame of video for better performance
        if process_this_frame:
            # Resize frame of video to 1/4 size for faster face recognition processing
            small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

            # Convert the image from BGR color to RGB
            rgb_small_frame = small_frame[:, :, ::-1]
            
            # Find all the faces and face encodings in the current frame of video
            face_locations = face_recognition.face_locations(rgb_small_frame)
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

            face_names = []
            for face_encoding in face_encodings:
                
                # See if the face is a match for the known face(s)
                matches = face_recognition.compare_faces(known_face_encodings, face_encoding, tolerance=0.35)
                name = "Unknown" # by default the person is considered unknown

              
                face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                best_match_index = np.argmin(face_distances)
                
                if matches[best_match_index]:
                    name = known_face_names[best_match_index]

                face_names.append(name)

        process_this_frame = not process_this_frame # skip next frame
                            # when its false, and you not it, becomes true


        # Display the results
        for (top, right, bottom, left), name in zip(face_locations, face_names):
            # revert downscaling face locations from 1/4 to 1/1
            top *= 4
            right *= 4
            bottom *= 4#`        -
            left *= 4

            if counter < 20:
            # Draw a box around the face
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

            else:
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)

            # Draw name label below the face

            font = cv2.FONT_HERSHEY_DUPLEX # cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

            if counter < 20:
                
                cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
                cv2.putText(frame, "verifying...", (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
            else:

                cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 255, 0), cv2.FILLED)
                cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

        # Display resulting image
        cv2.imshow('Video', frame)
        counter += 1


        # returning the final result, if the user does not match the face in the blockchain
        # then this is a false identity, otherwise it is verified person

        if counter == 40: # verify identity in 25 different frames before evaluating results
            if name != "Unknown":
                video_capture.release() # first we release the video capture
                cv2.destroyAllWindows() # close the stream windows
                return True
            else:
                video_capture.release() # first we release the video capture
                cv2.destroyAllWindows() # close the stream windows
                return False

        # Q to exit manually
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release handle to the webcam
    video_capture.release()
    cv2.destroyAllWindows()
