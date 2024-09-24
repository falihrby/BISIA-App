import numpy as np
from .common import draw_combined_box, draw_keypoints_for_debugging

def detect_bisindo_w(landmarks1, landmarks2, image, debug=True):
    if landmarks1 is None or landmarks2 is None:
        return False

    # Get image dimensions
    h, w, _ = image.shape

    # Extract coordinates for the thumbs (point 4) and index fingers (points 8, 7, 6) for both hands
    thumb_tip1 = np.array([landmarks1.landmark[4].x * w, landmarks1.landmark[4].y * h])
    thumb_tip2 = np.array([landmarks2.landmark[4].x * w, landmarks2.landmark[4].y * h])
    index_tip1 = np.array([landmarks1.landmark[8].x * w, landmarks1.landmark[8].y * h])
    index_pip1 = np.array([landmarks1.landmark[7].x * w, landmarks1.landmark[7].y * h])
    index_mcp1 = np.array([landmarks1.landmark[6].x * w, landmarks1.landmark[6].y * h])
    index_tip2 = np.array([landmarks2.landmark[8].x * w, landmarks2.landmark[8].y * h])
    index_pip2 = np.array([landmarks2.landmark[7].x * w, landmarks2.landmark[7].y * h])
    index_mcp2 = np.array([landmarks2.landmark[6].x * w, landmarks2.landmark[6].y * h])

    # Check if the index fingers are straight (points 8, 7, and 6 should form a straight line)
    def is_finger_straight(tip, pip, mcp, tolerance=0.1):
        vec1 = pip - tip
        vec2 = mcp - pip
        angle = np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))
        return angle > 1 - tolerance  # Check if the angle between them is close to 180 degrees

    # Check if both thumbs are pointing upwards (thumb Y-coordinates should be higher than wrist Y)
    is_thumb1_up = thumb_tip1[1] < landmarks1.landmark[0].y * h  # Thumb of the first hand is up
    is_thumb2_up = thumb_tip2[1] < landmarks2.landmark[0].y * h  # Thumb of the second hand is up

    # Ensure other fingers are folded
    def fingers_folded(landmarks):
        return all(landmarks.landmark[i].y > landmarks.landmark[i - 2].y for i in [12, 16, 20])

    are_other_fingers_folded1 = fingers_folded(landmarks1)
    are_other_fingers_folded2 = fingers_folded(landmarks2)

    # Check if thumbs are close enough (distance between thumb tips)
    thumb_distance = np.linalg.norm(thumb_tip1 - thumb_tip2)
    thumb_touch_threshold = 0.05 * w  # Dynamic threshold for "touching"

    # Detect if both index fingers are straight, thumbs are upwards and touching
    is_bisindo_w = (
        is_finger_straight(index_tip1, index_pip1, index_mcp1) and
        is_finger_straight(index_tip2, index_pip2, index_mcp2) and
        is_thumb1_up and
        is_thumb2_up and
        are_other_fingers_folded1 and
        are_other_fingers_folded2 and
        thumb_distance < thumb_touch_threshold
    )

    if is_bisindo_w:
        draw_combined_box(image, [landmarks1, landmarks2], "W", color=(0, 255, 0))

    # Optional debug visualization
    if debug:
        draw_keypoints_for_debugging(image, landmarks1, landmarks2)

    return is_bisindo_w
