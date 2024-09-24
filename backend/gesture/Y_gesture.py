import numpy as np
from .common import draw_combined_box, draw_keypoints_for_debugging

def detect_bisindo_y(landmarks1, landmarks2, image, debug=True):
    if landmarks1 is None or landmarks2 is None:
        return False

    # Get image dimensions
    h, w, _ = image.shape

    # Extract relevant coordinates for the 1st hand (forming "V" shape)
    index_tip1 = np.array([landmarks1.landmark[8].x * w, landmarks1.landmark[8].y * h])   # Index finger tip
    middle_tip1 = np.array([landmarks1.landmark[12].x * w, landmarks1.landmark[12].y * h]) # Middle finger tip
    wrist1 = np.array([landmarks1.landmark[0].x * w, landmarks1.landmark[0].y * h])       # Wrist of the 1st hand
    index_base1 = np.array([landmarks1.landmark[5].x * w, landmarks1.landmark[5].y * h])  # Index finger base (point 5)
    point2_1 = np.array([landmarks1.landmark[2].x * w, landmarks1.landmark[2].y * h])     # Point 2 of the 1st hand (base of the index finger)

    # Extract index finger tip of the 2nd hand
    index_tip2 = np.array([landmarks2.landmark[8].x * w, landmarks2.landmark[8].y * h])   # Index finger tip of the 2nd hand

    # Check if the index and middle fingers of the 1st hand form a "V" shape
    def is_v_shape(index_tip, middle_tip, wrist, tolerance=0.5):
        vec_index = index_tip - wrist
        vec_middle = middle_tip - wrist
        angle = np.dot(vec_index, vec_middle) / (np.linalg.norm(vec_index) * np.linalg.norm(vec_middle))
        return angle < 1 - tolerance  # Check if the angle between them is sufficiently less than 180 degrees to form a "V"

    # Check if the index tip of the 2nd hand is touching point 2 of the 1st hand
    def is_touching_point2(index_tip, point2, threshold=0.4):
        distance_to_point2 = np.linalg.norm(index_tip - point2)
        avg_hand_size = np.linalg.norm(wrist1 - index_base1)  # Hand size to adjust the threshold
        proximity_threshold = avg_hand_size * threshold
        return distance_to_point2 < proximity_threshold

    # Detect if the 1st hand is forming a "V" and the index finger of the 2nd hand is touching point 2
    is_v_formed = is_v_shape(index_tip1, middle_tip1, wrist1)
    is_touching = is_touching_point2(index_tip2, point2_1)

    # Detect the "Y" gesture
    is_bisindo_y = is_v_formed and is_touching

    if is_bisindo_y:
        draw_combined_box(image, [landmarks1, landmarks2], "Y", color=(0, 255, 0))

    # Optional debug visualization
    if debug:
        draw_keypoints_for_debugging(image, landmarks1, landmarks2)

    return is_bisindo_y
