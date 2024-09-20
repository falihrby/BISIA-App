import numpy as np
from .common import draw_combined_box, draw_keypoints_for_debugging  # Import both functions

def detect_bisindo_b(landmarks1, landmarks2, image, debug=True):
    # Ensure both hands are detected
    if landmarks1 is None or landmarks2 is None:
        return False

    # Extract landmarks for points 8, 12, 16 on the first hand (index, middle, ring finger tips)
    index_tip1 = np.array([landmarks1.landmark[8].x, landmarks1.landmark[8].y])
    middle_tip1 = np.array([landmarks1.landmark[12].x, landmarks1.landmark[12].y])
    ring_tip1 = np.array([landmarks1.landmark[16].x, landmarks1.landmark[16].y])

    # Extract landmarks for points 8, 5 on the second hand (index tip and index base)
    index_tip2 = np.array([landmarks2.landmark[8].x, landmarks2.landmark[8].y])
    index_base2 = np.array([landmarks2.landmark[5].x, landmarks2.landmark[5].y])

    # Calculate distances between fingers on the first hand to index tip and base on the second hand
    distance_index_tip = np.linalg.norm(index_tip1 - index_tip2)
    distance_middle_tip_index_base = np.linalg.norm(middle_tip1 - index_base2)
    distance_ring_tip_index_base = np.linalg.norm(ring_tip1 - index_base2)

    # Dynamic hand size calculation (for adaptable threshold)
    hand_size1 = np.linalg.norm(index_tip1 - np.array([landmarks1.landmark[0].x, landmarks1.landmark[0].y]))  # Distance from index tip to wrist
    hand_size2 = np.linalg.norm(index_tip2 - np.array([landmarks2.landmark[0].x, landmarks2.landmark[0].y]))  # Distance from index tip to wrist
    average_hand_size = (hand_size1 + hand_size2) / 2
    threshold_proximity = average_hand_size * 1.0  # Adjusted threshold for B gesture

    # Ensure the "B" shape is detected by checking the proximity of the points
    is_bisindo_b = (
        distance_index_tip < threshold_proximity and
        distance_middle_tip_index_base < threshold_proximity and
        distance_ring_tip_index_base < threshold_proximity
    )

    # Return true if all conditions for "B" are met
    if is_bisindo_b:
        draw_combined_box(image, [landmarks1, landmarks2], "B", color=(0, 255, 0))

        # Optional Debug Visualization
        if debug:
            draw_keypoints_for_debugging(image, landmarks1, landmarks2)

        return True

    # Optional Debug Visualization (if "B" is not detected)
    if debug:
        draw_keypoints_for_debugging(image, landmarks1, landmarks2)

    return False
