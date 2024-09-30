import numpy as np
import cv2
from .common import draw_combined_box, draw_keypoints_for_debugging  # Import both functions

def detect_bisindo_t(landmarks1, landmarks2, image, debug=False):
    if landmarks1 is None or landmarks2 is None:
        return False

    # Extract key landmarks for both hands
    point_6_hand1 = np.array([landmarks1.landmark[6].x, landmarks1.landmark[6].y])   # Point 6 on hand 1 (MCP of index finger)
    point_8_hand2 = np.array([landmarks2.landmark[8].x, landmarks2.landmark[8].y])   # Point 8 on hand 2 (Index fingertip)

    # Calculate the distance between point 6 of hand 1 and point 8 of hand 2
    distance_point_6_to_point_8 = np.linalg.norm(point_6_hand1 - point_8_hand2)

    # Calculate hand size to set a dynamic threshold
    hand_size_1 = np.linalg.norm(np.array([landmarks1.landmark[0].x, landmarks1.landmark[0].y]) - point_6_hand1)  # Hand 1 size as reference
    hand_size_2 = np.linalg.norm(np.array([landmarks2.landmark[0].x, landmarks2.landmark[0].y]) - point_8_hand2)  # Hand 2 size as reference

    # Set a dynamic threshold for detecting the touch
    t_shape_threshold = (hand_size_1 + hand_size_2) / 2 * 0.3

    # Check if point 6 of hand 1 is touching point 8 of hand 2
    is_t_shape = distance_point_6_to_point_8 < t_shape_threshold

    # Final condition: If the thumb and index fingertips are touching
    if is_t_shape:
        draw_combined_box(image, [landmarks1, landmarks2], "T", color=(0, 255, 0))

        # Optional: Debug visualization of keypoints
        if debug:
            draw_keypoints_for_debugging(image, landmarks1, landmarks2)
        
        return True

    # Optional: Debug visualization even if "T" is not detected
    if debug:
        draw_keypoints_for_debugging(image, landmarks1, landmarks2)

    return False
