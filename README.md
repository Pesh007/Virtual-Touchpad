# Virtual Touchpad

Virtual Touchpad allows you to control your mouse using hand gestures captured by a webcam. The project is designed to let you move the cursor, click, and scroll without using a physical mouse or trackpad, making it usable even while lying in bed.

The system uses MediaPipe Hand Landmarker for real-time hand tracking and interprets finger configurations as gestures.

# Description

The cursor is controlled by moving your hand while extending only the index finger. A left mouse click is triggered by pinching the tips of the thumb and the middle finger. Scrolling is performed by extending both the index and middle fingers and moving the hand vertically or horizontally.

<img width="353" height="517" alt="image" src="https://github.com/user-attachments/assets/844ec6cb-3c52-4b31-a170-ab06b7ceb0de" />
<img width="368" height="600" alt="image" src="https://github.com/user-attachments/assets/5de777e8-e634-48a1-9efd-d5333fed11d3" />
<img width="410" height="614" alt="image" src="https://github.com/user-attachments/assets/95678c1d-3195-42e4-8f5b-11c8fe0d79ee" />


The application runs locally and processes the camera feed in real time.

# Requirements

You must download the hand_landmarker.task model from the following page and place it in the project directory:

https://ai.google.dev/edge/mediapipe/solutions/vision/hand_landmarker

All required Python packages can be installed using:
'''
pip install -r requirements.txt
'''

A working webcam is required.

# Usage

Run the main script:

python virtualTouchpad.py


At the moment, if the video preview window is disabled, the application can only be stopped from the terminal.

# Problems

The application currently uses a significant amount of CPU due to real-time video processing and Python overhead. Gesture detection can be sensitive to lighting conditions and hand positioning. There is no clean shutdown mechanism when the video preview is disabled.

# Planned Improvements

Future work includes reducing CPU usage, improving gesture recognition reliability, implementing smoother and non-linear scrolling behavior, adding a proper shutdown mechanism, and creating a graphical user interface.

# Notes

This project is experimental and intended primarily for learning and prototyping. Performance and behavior may vary depending on hardware and environmental conditions. mouseControls.dll is build with dllmain.cpp with Visual Studio
