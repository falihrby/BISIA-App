import numpy as np
from .common import draw_combined_box, draw_keypoints_for_debugging

def detect_bisindo_v(landmarks1, image, debug=False):
    if landmarks1 is None:
        return False

    # Get image dimensions
    h, w, _ = image.shape

    # Extract coordinates for the thumb (point 4) and index finger joints (points 8, 7, 6)
    thumb_tip = np.array([landmarks1.landmark[4].x * w, landmarks1.landmark[4].y * h])
    index_tip = np.array([landmarks1.landmark[8].x * w, landmarks1.landmark[8].y * h])
    index_pip = np.array([landmarks1.landmark[7].x * w, landmarks1.landmark[7].y * h])
    index_mcp = np.array([landmarks1.landmark[6].x * w, landmarks1.landmark[6].y * h])

    # Check if the index finger is straight (points 8, 7, and 6 should form a straight line)
    def is_finger_straight(tip, pip, mcp, tolerance=0.5):
        vec1 = pip - tip
        vec2 = mcp - pip
        angle = np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))
        return angle > 1 - tolerance  # Check if the angle between them is close to 180 degrees

    # Ensure the thumb is pointing upwards (thumb tip Y-coordinate should be lower than index finger joints)
    is_thumb_up = thumb_tip[1] < landmarks1.landmark[0].y * h  # Check if the thumb is higher than the wrist (point 0)

    # Ensure other fingers are folded
    def fingers_folded(landmarks):
        return all(landmarks.landmark[i].y > landmarks.landmark[i - 2].y for i in [12, 16, 20])

    are_other_fingers_folded = fingers_folded(landmarks1)

    # Detect if the index finger is straight and the thumb is up
    is_bisindo_v = is_finger_straight(index_tip, index_pip, index_mcp) and is_thumb_up and are_other_fingers_folded

    if is_bisindo_v:
        draw_combined_box(image, [landmarks1], "V", color=(0, 255, 0))

    # Optional debug visualization
    if debug:
        draw_keypoints_for_debugging(image, landmarks1)

    return is_bisindo_v
