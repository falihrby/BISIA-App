import numpy as np
from .common import draw_combined_box, draw_keypoints_for_debugging  # Import both functions

def detect_bisindo_r(landmarks1, image, debug=True):
    if landmarks1 is None:
        return False

    # Extract key landmarks for the hand
    index_tip = np.array([landmarks1.landmark[8].x, landmarks1.landmark[8].y])     # Index fingertip (point 8)
    middle_tip = np.array([landmarks1.landmark[12].x, landmarks1.landmark[12].y])  # Middle fingertip (point 12)
    thumb_tip = np.array([landmarks1.landmark[4].x, landmarks1.landmark[4].y])     # Thumb tip (point 4)
    ring_tip = np.array([landmarks1.landmark[16].x, landmarks1.landmark[16].y])    # Ring fingertip (point 16)
    little_tip = np.array([landmarks1.landmark[20].x, landmarks1.landmark[20].y])  # Little fingertip (point 20)
    wrist = np.array([landmarks1.landmark[0].x, landmarks1.landmark[0].y])         # Wrist (point 0)

    # Calculate distances to determine whether the fingers are open or closed
    hand_size = np.linalg.norm(index_tip - wrist)  # Use the index finger and wrist distance as a reference for hand size
    dynamic_threshold = hand_size * 0.4  # Threshold for determining if a finger is bent or extended

    # Check if the middle fingertip and thumb tip are touching
    distance_middle_to_thumb = np.linalg.norm(middle_tip - thumb_tip)
    is_touching = distance_middle_to_thumb < dynamic_threshold

    # Check if the index finger is open (distance between index tip and wrist is large)
    is_index_open = np.linalg.norm(index_tip - wrist) > hand_size * 0.8

    # Check if the ring and little fingers are closed (distance between ring/little tips and wrist is small)
    is_ring_closed = np.linalg.norm(ring_tip - wrist) < dynamic_threshold
    is_little_closed = np.linalg.norm(little_tip - wrist) < dynamic_threshold

    # Final condition: index finger is open, middle and thumb touch, ring and little fingers are closed
    if is_touching and is_index_open and is_ring_closed and is_little_closed:
        draw_combined_box(image, [landmarks1], "R", color=(0, 255, 0))

        # Optional: Debug visualization of keypoints
        if debug:
            draw_keypoints_for_debugging(image, landmarks1)
        
        return True

    # Optional: Debug visualization even if "R" is not detected
    if debug:
        draw_keypoints_for_debugging(image, landmarks1)

    return False
