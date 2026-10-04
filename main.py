import cv2
import face_recognition
import os
import numpy as np
from datetime import datetime

# 1. Load known faces
path = 'known_faces'
known_encodings = []
known_names = []

for cl in os.listdir(path):
    curImg = cv2.imread(f'{path}/{cl}')
    # Convert from BGR (OpenCV) to RGB (face_recognition)
    imgRGB = cv2.cvtColor(curImg, cv2.COLOR_BGR2RGB)
    encode = face_recognition.face_encodings(imgRGB)[0]
    known_encodings.append(encode)
    known_names.append(os.path.splitext(cl)[0])

# 2. Function to log attendance
def markAttendance(name):
    with open('Attendance.csv', 'r+') as f:
        myDataList = f.readlines()
        nameList = [line.split(',')[0] for line in myDataList]
        
        if name not in nameList:
            now = datetime.now()
            dtString = now.strftime('%Y-%m-%d %H:%M:%S')
            f.writelines(f'\n{name},{dtString}')

# 3. Start Webcam
cap = cv2.VideoCapture(0)

while True:
    success, img = cap.read()
    imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25) # Scale down for faster processing
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

    facesCurFrame = face_recognition.face_locations(imgS)
    encodesCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)

    for encodeFace, faceLoc in zip(encodesCurFrame, facesCurFrame):
        matches = face_recognition.compare_faces(known_encodings, encodeFace)
        faceDis = face_recognition.face_distance(known_encodings, encodeFace)
        matchIndex = np.argmin(faceDis)

        if matches[matchIndex]:
            name = known_names[matchIndex].upper()
            
            # Draw bounding box
            y1, x2, y2, x1 = faceLoc
            y1, x2, y2, x1 = y1*4, x2*4, y2*4, x1*4 # Scale back up
            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(img, name, (x1+6, y2-6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
            
            markAttendance(name)

    cv2.imshow('Webcam', img)
    if cv2.waitKey(1) & 0xFF == ord('q'): # Press 'q' to quit
        break
        
cap.release()
cv2.destroyAllWindows()