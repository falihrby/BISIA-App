import numpy as np
from .common import draw_combined_box, draw_keypoints_for_debugging  # Import both functions

def detect_bisindo_p(landmarks1, landmarks2, image, debug=True):
    if landmarks1 is None or landmarks2 is None:
        return False

    # Extract points 8 (index fingertip) and 7 (PIP joint) from the 1st hand
    index_tip_1 = np.array([landmarks1.landmark[8].x, landmarks1.landmark[8].y])  # Hand 1, index fingertip
    index_pip_1 = np.array([landmarks1.landmark[7].x, landmarks1.landmark[7].y])  # Hand 1, PIP joint

    # Extract points 8 (index fingertip) and 4 (thumb tip) from the 2nd hand
    index_tip_2 = np.array([landmarks2.landmark[8].x, landmarks2.landmark[8].y])  # Hand 2, index fingertip
    thumb_tip_2 = np.array([landmarks2.landmark[4].x, landmarks2.landmark[4].y])  # Hand 2, thumb tip

    # Calculate distances between the required points
    distance_index_tip_to_index_tip = np.linalg.norm(index_tip_1 - index_tip_2)  # Distance between index tips
    distance_pip_to_thumb_tip = np.linalg.norm(index_pip_1 - thumb_tip_2)        # Distance between PIP (hand 1) and thumb tip (hand 2)

    # Dynamic hand size scaling based on the size of hand 1
    hand_size_1 = np.linalg.norm(index_tip_1 - index_pip_1)  # Distance between index tip and PIP on hand 1
    dynamic_threshold = hand_size_1 * 0.9  # Adjusted threshold for more accurate P gesture detection

    # Check if the index fingertip (point 8) and PIP (point 7) on the 1st hand are touching
    # the index fingertip (point 8) and thumb tip (point 4) on the 2nd hand
    is_fingers_touching = (
        distance_index_tip_to_index_tip < dynamic_threshold and  # Index tips of both hands are close
        distance_pip_to_thumb_tip < dynamic_threshold  # PIP of hand 1 and thumb tip of hand 2 are close
    )

    # Check if all conditions for the letter "P" are met
    if is_fingers_touching:
        draw_combined_box(image, [landmarks1, landmarks2], "P", color=(0, 255, 0))

        # Optional: Debug visualization of keypoints
        if debug:
            draw_keypoints_for_debugging(image, landmarks1, landmarks2)
        
        return True

    # Optional: Debug visualization even if "P" is not detected
    if debug:
        draw_keypoints_for_debugging(image, landmarks1, landmarks2)

    return False
