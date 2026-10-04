import streamlit as st
import cv2
import face_recognition
import numpy as np
import pandas as pd
from datetime import datetime
import os

st.set_page_config(page_title="Attendance Dashboard", layout="wide")
st.title("Live Attendance System")

# Function to mark attendance in CSV
def mark_attendance(name):
    with open('Attendance.csv', 'r+') as f:
        myDataList = f.readlines()
        nameList = [line.split(',')[0] for line in myDataList]
        if name not in nameList:
            now = datetime.now()
            dtString = now.strftime('%Y-%m-%d %H:%M:%S')
            f.writelines(f'\n{name},{dtString}')

# Load known face
known_image = face_recognition.load_image_file("Known_faces/faheem.jpg")
known_encode = face_recognition.face_encodings(known_image)[0]
known_encodings = [known_encode]
known_names = ["Faheem"]

# Build the layout
col1, col2 = st.columns(2)

with col1:
    st.header("Webcam Feed")
    # Toggle switch to start/stop the camera
    run_camera = st.checkbox("Turn on Camera")
    frame_placeholder = st.empty()

with col2:
    st.header("Attendance Log")
    log_placeholder = st.empty()

# Initialize the webcam
camera = cv2.VideoCapture(0)

while run_camera:
    success, img = camera.read()
    if not success:
        st.error("Failed to capture video from webcam.")
        break
        
    # Process the frame for face recognition
    imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    imgRGB = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)
    
    facesCurFrame = face_recognition.face_locations(imgRGB)
    encodesCurFrame = face_recognition.face_encodings(imgRGB, facesCurFrame)
    
    for encodeFace, faceLoc in zip(encodesCurFrame, facesCurFrame):
        matches = face_recognition.compare_faces(known_encodings, encodeFace)
        faceDis = face_recognition.face_distance(known_encodings, encodeFace)
        matchIndex = np.argmin(faceDis)
        
        if matches[matchIndex]:
            name = known_names[matchIndex].upper()
            
            # Draw the bounding box
            y1, x2, y2, x1 = faceLoc
            y1, x2, y2, x1 = y1*4, x2*4, y2*4, x1*4
            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(img, name, (x1+6, y2-6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
            
            # Log the data
            mark_attendance(name)

    # Convert final image back to RGB for Streamlit and display it
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    frame_placeholder.image(img, channels="RGB")
    
    # Read the CSV and update the web table in real-time
    try:
        df = pd.read_csv('Attendance.csv', names=['Name', 'Timestamp'])
        log_placeholder.dataframe(df, use_container_width=True)
    except Exception:
        pass
else:
    # Release the camera safely when the checkbox is turned off
    camera.release()