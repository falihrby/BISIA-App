# backend/handGestureRecognition.py
import cv2
import mediapipe as mp
import numpy as np
import logging

# Import gesture detection functions
from gesture.A_gesture import detect_bisindo_a
from gesture.B_gesture import detect_bisindo_b
from gesture.C_gesture import detect_bisindo_c
from gesture.D_gesture import detect_bisindo_d
from gesture.E_gesture import detect_bisindo_e
from gesture.F_gesture import detect_bisindo_f
from gesture.G_gesture import detect_bisindo_g
from gesture.H_gesture import detect_bisindo_h
from gesture.I_gesture import detect_bisindo_i
from gesture.J_gesture import detect_bisindo_j
from gesture.K_gesture import detect_bisindo_k
from gesture.L_gesture import detect_bisindo_l
from gesture.M_gesture import detect_bisindo_m
from gesture.N_gesture import detect_bisindo_n
from gesture.O_gesture import detect_bisindo_o
from gesture.P_gesture import detect_bisindo_p
from gesture.Q_gesture import detect_bisindo_q
from gesture.R_gesture import detect_bisindo_r
from gesture.S_gesture import detect_bisindo_s
from gesture.T_gesture import detect_bisindo_t
from gesture.U_gesture import detect_bisindo_u
from gesture.V_gesture import detect_bisindo_v
from gesture.W_gesture import detect_bisindo_w
from gesture.X_gesture import detect_bisindo_x
from gesture.Y_gesture import detect_bisindo_y
from gesture.Z_gesture import detect_bisindo_z

# Initialize MediaPipe hands model
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

# Configure logging
logging.basicConfig(level=logging.INFO)

def process_frame(frame):
    """Process the captured frame to detect hand gestures and draw landmarks."""
    image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    with mp_hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5, max_num_hands=2) as hands:
        results = hands.process(image_rgb)

        image = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2BGR)
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                # Adjust circle size and thickness for landmarks and connections
                mp_drawing.draw_landmarks(
                    image,
                    hand_landmarks,
                    mp_hands.HAND_CONNECTIONS,
                    mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=1, circle_radius=2),  # integer values
                    mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=1, circle_radius=2)   # integer values
                )

            landmarks1 = results.multi_hand_landmarks[0]
            landmarks2 = results.multi_hand_landmarks[1] if len(results.multi_hand_landmarks) > 1 else None

            gesture_detected, label = detect_and_display_gesture(landmarks1, landmarks2, image)
            return gesture_detected, label, image
        else:
            # No landmarks detected, return the original image
            return False, None, frame

def detect_and_display_gesture(landmarks1, landmarks2, image):
    """Detect gestures and display the result on the image."""
    gesture_detected = False
    label = None

    gesture_mapping_single = [
        (detect_bisindo_e, "Huruf E Terdeteksi"),
        (detect_bisindo_i, "Huruf I Terdeteksi"),
        (detect_bisindo_c, "Huruf C Terdeteksi"),
        (detect_bisindo_o, "Huruf O Terdeteksi"),
        (detect_bisindo_u, "Huruf U Terdeteksi"),
        (detect_bisindo_l, "Huruf L Terdeteksi"),
        (detect_bisindo_r, "Huruf R Terdeteksi"),
        (detect_bisindo_j, "Huruf J Terdeteksi"),
        (detect_bisindo_z, "Huruf Z Terdeteksi"),
        (detect_bisindo_v, "Huruf V Terdeteksi")
    ]

    gesture_mapping_double = [
        (detect_bisindo_a, "Huruf A Terdeteksi"),
        (detect_bisindo_m, "Huruf M Terdeteksi"),
        (detect_bisindo_n, "Huruf N Terdeteksi"),
        (detect_bisindo_d, "Huruf D Terdeteksi"),
        (detect_bisindo_p, "Huruf P Terdeteksi"),
        (detect_bisindo_b, "Huruf B Terdeteksi"),
        (detect_bisindo_h, "Huruf H Terdeteksi"),
        (detect_bisindo_s, "Huruf S Terdeteksi"),
        (detect_bisindo_k, "Huruf K Terdeteksi"),
        (detect_bisindo_t, "Huruf T Terdeteksi"),
        (detect_bisindo_g, "Huruf G Terdeteksi"),
        (detect_bisindo_y, "Huruf Y Terdeteksi"),
        (detect_bisindo_f, "Huruf F Terdeteksi"),
        (detect_bisindo_w, "Huruf W Terdeteksi"),
        (detect_bisindo_q, "Huruf Q Terdeteksi"),
        (detect_bisindo_x, "Huruf X Terdeteksi")
    ]

    if landmarks2:
        for detect_fn, text in gesture_mapping_double:
            if detect_fn(landmarks1, landmarks2, image):
                label = text
                gesture_detected = True
                break
    else:
        for detect_fn, text in gesture_mapping_single:
            if detect_fn(landmarks1, image):
                label = text
                gesture_detected = True
                break

    return gesture_detected, label
