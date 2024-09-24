import numpy as np
from .common import draw_combined_box, draw_keypoints_for_debugging  # Adjust path based on your project structure

def detect_bisindo_q(landmarks1, landmarks2, image, debug=True):
    if landmarks1 is None or landmarks2 is None:
        return False

    # Extract key landmarks
    index_tip_1 = np.array([landmarks1.landmark[8].x, landmarks1.landmark[8].y])  # Index tip on hand 1
    thumb_tip_1 = np.array([landmarks1.landmark[4].x, landmarks1.landmark[4].y])  # Thumb tip on hand 1
    index_tip_2 = np.array([landmarks2.landmark[8].x, landmarks2.landmark[8].y])  # Index tip on hand 2

    # Calculate distances between points on hand 1 (index and thumb must touch)
    distance_index_to_thumb_1 = np.linalg.norm(index_tip_1 - thumb_tip_1)  # Distance between index and thumb on hand 1

    # Calculate distances from index tip on hand 2 to points on hand 1 (index and thumb)
    distance_index_2_to_index_1 = np.linalg.norm(index_tip_2 - index_tip_1)  # Distance between index tip of hand 2 and index tip of hand 1
    distance_index_2_to_thumb_1 = np.linalg.norm(index_tip_2 - thumb_tip_1)  # Distance between index tip of hand 2 and thumb tip of hand 1

    # Define thresholds for "touching" detection
    touch_threshold = 0.2  # Threshold for detecting if the points are close enough to be considered "touching"

    # Check if index and thumb on hand 1 are touching
    is_touching_on_hand_1 = distance_index_to_thumb_1 < touch_threshold

    # Check if index on hand 2 is touching both index and thumb on hand 1
    is_touching_on_hand_2 = (
        distance_index_2_to_index_1 < touch_threshold and
        distance_index_2_to_thumb_1 < touch_threshold
    )

    # If both conditions are satisfied, detect the letter "Q"
    if is_touching_on_hand_1 and is_touching_on_hand_2:
        draw_combined_box(image, [landmarks1, landmarks2], "Q", color=(0, 255, 0))

        # Optional: Debug visualization of keypoints
        if debug:
            draw_keypoints_for_debugging(image, landmarks1, landmarks2)
        
        return True

    # Optional: Debug visualization even if "Q" is not detected
    if debug:
        draw_keypoints_for_debugging(image, landmarks1, landmarks2)

    return False
