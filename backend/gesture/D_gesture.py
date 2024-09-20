import numpy as np
from .common import draw_combined_box, draw_keypoints_for_debugging  # Import both functions

def detect_bisindo_d(landmarks1, landmarks2, image, debug=True):
    if landmarks1 is None or landmarks2 is None:
        return False

    # Extract landmarks for points 8 and 4 on the first hand (index tip and thumb tip)
    index_tip1 = np.array([landmarks1.landmark[8].x, landmarks1.landmark[8].y])  # Point 8 on hand 1 (index tip)
    thumb_tip1 = np.array([landmarks1.landmark[4].x, landmarks1.landmark[4].y])  # Point 4 on hand 1 (thumb tip)

    # Extract landmarks for points 8 and 5 on the second hand (index tip and index base)
    index_tip2 = np.array([landmarks2.landmark[8].x, landmarks2.landmark[8].y])  # Point 8 on hand 2 (index tip)
    index_base2 = np.array([landmarks2.landmark[5].x, landmarks2.landmark[5].y])  # Point 5 on hand 2 (index base)

    # Calculate distances between relevant points on both hands
    distance_index_tip = np.linalg.norm(index_tip1 - index_tip2)  # Distance between index tip of hand 1 and hand 2
    distance_thumb_tip_index_base = np.linalg.norm(thumb_tip1 - index_base2)  # Distance between thumb tip of hand 1 and index base of hand 2

    # Dynamic hand size calculation (for adaptable threshold)
    hand_size1 = np.linalg.norm(index_tip1 - np.array([landmarks1.landmark[0].x, landmarks1.landmark[0].y]))  # Distance from index tip to wrist on hand 1
    hand_size2 = np.linalg.norm(index_tip2 - np.array([landmarks2.landmark[0].x, landmarks2.landmark[0].y]))  # Distance from index tip to wrist on hand 2
    average_hand_size = (hand_size1 + hand_size2) / 2
    threshold_proximity = average_hand_size * 0.7  # Adjusted threshold for D gesture

    # Ensure the "D" shape is detected by checking the proximity of the points
    is_bisindo_d = (
        distance_index_tip < threshold_proximity and  # Index tips of both hands are close
        distance_thumb_tip_index_base < threshold_proximity  # Thumb tip of hand 1 is close to the index base of hand 2
    )

    # If the "D" gesture is detected, draw a box around both hands
    if is_bisindo_d:
        draw_combined_box(image, [landmarks1, landmarks2], "D", color=(0, 255, 0))

        # Optional Debug Visualization
        if debug:
            draw_keypoints_for_debugging(image, landmarks1, landmarks2)

        return True

    # Optional Debug Visualization (if "D" is not detected)
    if debug:
        draw_keypoints_for_debugging(image, landmarks1, landmarks2)

    return False
