import cv2
import time
import math
import mediapipe as mp
from mediapipe.tasks.python import vision
from mediapipe.tasks import python

from OneEuroFilter import OneEuroFilter

import pyautogui
from mouseControls import move_mouse, left_click, horizontal_scroll, vertical_scroll



# MediaPipe Hand Landmarker setup


BaseOptions = python.BaseOptions
HandLandmarker = vision.HandLandmarker
HandLandmarkerOptions = vision.HandLandmarkerOptions
RunningMode = vision.RunningMode

hand_options = HandLandmarkerOptions(
    base_options=BaseOptions(model_asset_path="hand_landmarker.task"),
    running_mode=RunningMode.VIDEO,
    num_hands=1
)


# Webcam setup


cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1240)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 960)



# Gesture detection 


def is_showing_one(landmarks):
    """Index finger extended, others folded"""
    return (
        landmarks[8].y < landmarks[6].y and
        landmarks[12].y > landmarks[10].y and
        landmarks[16].y > landmarks[14].y and
        landmarks[20].y > landmarks[18].y
    )


def is_showing_two(landmarks):
    """Index + middle extended, others folded"""
    return (
        landmarks[8].y  < landmarks[6].y and
        landmarks[12].y < landmarks[10].y and
        landmarks[16].y > landmarks[14].y and
        landmarks[20].y > landmarks[18].y
    )


def is_middle_thumb_pinch(
    landmarks,
    thumb_x_filter,
    thumb_y_filter,
    middle_x_filter,
    middle_y_filter,
    threshold
):
    """Thumb tip touching middle finger tip"""
    dx = thumb_x_filter.filter(landmarks[4].x) - middle_x_filter.filter(landmarks[12].x)
    dy = thumb_y_filter.filter(landmarks[4].y) - middle_y_filter.filter(landmarks[12].y)
    return math.sqrt(dx * dx + dy * dy) < threshold



# Screen & gesture state


screen_width, screen_height = pyautogui.size()

gesture_start_frame_pos = None

# Gesture state flags
first_time_pointing = True
first_time_scrolling = True

# Per-gesture inactivity counters
frames_without_pointing = 0
frames_without_scrolling = 0

# Click timing
click_frame_counter = 0


# Filters


index_x_filter = OneEuroFilter(freq=30, mincutoff=1, beta=0.0001)
index_y_filter = OneEuroFilter(freq=30, mincutoff=1, beta=0.0001)

middle_x_filter = OneEuroFilter(freq=30, mincutoff=1, beta=0.0001)
middle_y_filter = OneEuroFilter(freq=30, mincutoff=1, beta=0.0001)

thumb_x_filter = OneEuroFilter(freq=30, mincutoff=1, beta=0.0001)
thumb_y_filter = OneEuroFilter(freq=30, mincutoff=1, beta=0.0001)



# Main loop


frame_counter = 0
start_time = time.time()

with HandLandmarker.create_from_options(hand_options) as landmarker:
    while cap.isOpened():
        frame_counter += 1

        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.flip(frame, 1)
        h, w, _ = frame.shape

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb)

        timestamp_ms = int(time.time() * 1000)
        result = landmarker.detect_for_video(mp_image, timestamp_ms)

        if result.hand_landmarks:
            for landmarks in result.hand_landmarks:


                # POINTING 

                if is_showing_one(landmarks):
                    frames_without_pointing = 0
                    click_frame_counter += 1
                    frames_without_scrolling += 1


                    if is_middle_thumb_pinch(
                        landmarks,
                        thumb_x_filter,
                        thumb_y_filter,
                        middle_x_filter,
                        middle_y_filter,
                        threshold=finger_extension_distance / 5
                    ) and click_frame_counter > 20:
                        click_frame_counter = 0
                        left_click()

                    index_tip = landmarks[8]
                    index_base = landmarks[5]

                    x = int(index_tip.x * w)
                    y = int(index_tip.y * h)

                    if first_time_pointing:
                        first_time_pointing = False
                        gesture_start_frame_pos = [x, y]

                    finger_extension_distance = abs(index_base.y - index_tip.y)

                    cursor_x = (
                        screen_width // 2
                        - (gesture_start_frame_pos[0] - x)
                        * 500
                        / finger_extension_distance
                        / w
                    )

                    cursor_y = (
                        screen_height // 2
                        - (gesture_start_frame_pos[1] - y)
                        * 500
                        / finger_extension_distance
                        / h
                    )

                    cursor_x = index_x_filter.filter(cursor_x)
                    cursor_y = index_y_filter.filter(cursor_y)

                    move_mouse(int(cursor_x), int(cursor_y))

                # SCROLLING 

                elif is_showing_two(landmarks):
                    frames_without_scrolling = 0
                    frames_without_pointing += 1

                    index_tip = landmarks[8]
                    middle_tip = landmarks[12]

                    ix = int(index_tip.x * w)
                    iy = int(index_tip.y * h)

                    mx = int(middle_tip.x * w)
                    my = int(middle_tip.y * h)

                    avg_x = (ix + mx) // 2
                    avg_y = (iy + my) // 2

                    finger_spacing = abs(ix - mx)

                    if first_time_scrolling:
                        first_time_scrolling = False
                        gesture_start_frame_pos = [avg_x, avg_y]

                    vertical_scroll(-int((avg_y - gesture_start_frame_pos[1]) / finger_spacing * 40))
                    horizontal_scroll(int((avg_x - gesture_start_frame_pos[0]) / finger_spacing * 40))


                # NO MATCHING GESTURE

                else:
                    frames_without_pointing += 1
                    frames_without_scrolling += 1

                    if frames_without_pointing > 8:
                        first_time_pointing = True
                        index_x_filter.reset()
                        index_y_filter.reset()

                    if frames_without_scrolling > 8:
                        first_time_scrolling = True

        # GUI intentionally disabled for performance




end_time = time.time()
print("Average frame time:", (end_time - start_time) / frame_counter)

cap.release()
cv2.destroyAllWindows()


