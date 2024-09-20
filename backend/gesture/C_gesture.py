import numpy as np
from .common import draw_combined_box, draw_keypoints_for_debugging  # Import both functions

def detect_bisindo_c(landmarks1, image, debug=False):
    if landmarks1 is None:
        return False

    # Extract landmarks for index finger and thumb
    index_tip = np.array([landmarks1.landmark[8].x, landmarks1.landmark[8].y])
    index_mid = np.array([landmarks1.landmark[6].x, landmarks1.landmark[6].y])
    thumb_tip = np.array([landmarks1.landmark[4].x, landmarks1.landmark[4].y])
    thumb_mid = np.array([landmarks1.landmark[3].x, landmarks1.landmark[3].y])

    # Calculate distances and angle between index and thumb
    distance_index_tip_thumb_tip = np.linalg.norm(index_tip - thumb_tip)
    distance_index_mid_thumb_mid = np.linalg.norm(index_mid - thumb_mid)

    # Calculate the angle between the index finger and thumb
    index_vector = index_tip - index_mid
    thumb_vector = thumb_tip - thumb_mid
    angle_between = np.degrees(np.arccos(np.dot(index_vector, thumb_vector) / 
                            (np.linalg.norm(index_vector) * np.linalg.norm(thumb_vector) + 1e-6)))  # Stability with epsilon

    # Check if the index finger is curled toward the thumb
    is_c_shape = (
        distance_index_tip_thumb_tip < 0.8 and
        distance_index_mid_thumb_mid < 0.8 and
        40 < angle_between < 70
    )

    # Ensure that middle, ring, and pinky fingers are closed
    are_other_fingers_folded = (
        landmarks1.landmark[12].y > landmarks1.landmark[10].y and  # Middle finger
        landmarks1.landmark[16].y > landmarks1.landmark[14].y and  # Ring finger
        landmarks1.landmark[20].y > landmarks1.landmark[18].y      # Pinky finger
    )

    # "C" is detected only if index is curled and other fingers are folded
    if is_c_shape and are_other_fingers_folded:
        draw_combined_box(image, [landmarks1], "C", color=(0, 255, 0))

        # Debug visualization
        if debug:
            draw_keypoints_for_debugging(image, landmarks1)

        return True

    # If gesture not detected and debugging is enabled, visualize keypoints
    if debug:
        draw_keypoints_for_debugging(image, landmarks1)

    return False
