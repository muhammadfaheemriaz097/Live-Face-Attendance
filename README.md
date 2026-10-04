# Live Face Recognition Attendance System

A real-time, web-based facial recognition dashboard that automatically detects users via webcam and logs their attendance with timestamps. Built with Python, OpenCV, and Streamlit, this project provides a seamless interface for biometric tracking.

## Features
* **Real-Time Detection:** Processes live webcam feeds to encode and match faces instantly.
* **Streamlit Web Dashboard:** Replaces standard OpenCV popup windows with an interactive browser UI.
* **Automated Data Logging:** Updates a CSV attendance registry dynamically using Pandas.
* **Duplicate Prevention:** Ensures users are only logged once per session.

## Technologies Used
* **Language:** Python 3.14
* **Computer Vision:** OpenCV (`opencv-python`), `face_recognition`
* **Web Framework:** Streamlit
* **Data Processing:** Pandas, NumPy

## Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/muhammadfaheemriaz097/Live-Face-Attendance.git](https://github.com/muhammadfaheemriaz097/Live-Face-Attendance.git)
   cd Live-Face-Attendance

2. **Install core dependencies:**
```bash
python -m pip install streamlit pandas opencv-python numpy
3. **Install Face Recognition and setuptools workaround:**
*Note: Python 3.14 requires an older version of setuptools for the dlib/face_recognition models to locate their cached files correctly.*
```bash
python -m pip install "setuptools<70.0.0"
python -m pip install face_recognition

## Usage

1. Place a clear `.jpg` image of the authorized person inside the `Known_faces/` directory and name it with their first name (e.g., `faheem.jpg`).
2. Launch the Streamlit server:
```bash
python -m streamlit run app.py

3. Check the "Turn on Camera" box in the browser dashboard to begin tracking.

**Author:** Muhammad Faheem Riaz

*Machine Learning and Artificial Intelligence Engineer*
