import numpy as np
from .common import draw_combined_box, draw_keypoints_for_debugging  # Import both functions

def detect_bisindo_s(landmarks1, landmarks2, image, debug=False):
    if landmarks1 is None or landmarks2 is None:
        return False

    # Extract key landmarks for both hands
    thumb_tip_1 = np.array([landmarks1.landmark[4].x, landmarks1.landmark[4].y])  # Thumb tip on hand 1
    index_tip_1 = np.array([landmarks1.landmark[8].x, landmarks1.landmark[8].y])  # Index tip on hand 1
    
    thumb_tip_2 = np.array([landmarks2.landmark[4].x, landmarks2.landmark[4].y])  # Thumb tip on hand 2
    index_tip_2 = np.array([landmarks2.landmark[8].x, landmarks2.landmark[8].y])  # Index tip on hand 2

    # Calculate distance between thumb and index on both hands (to form "C" shapes)
    distance_thumb_index_1 = np.linalg.norm(thumb_tip_1 - index_tip_1)  # Distance between thumb and index on hand 1
    distance_thumb_index_2 = np.linalg.norm(thumb_tip_2 - index_tip_2)  # Distance between thumb and index on hand 2

    # Define dynamic thresholds based on the size of the hands (relaxed thresholds for more leeway)
    hand_size_1 = np.linalg.norm(np.array([landmarks1.landmark[0].x, landmarks1.landmark[0].y]) - thumb_tip_1)  # Hand 1 size
    hand_size_2 = np.linalg.norm(np.array([landmarks2.landmark[0].x, landmarks2.landmark[0].y]) - thumb_tip_2)  # Hand 2 size

    # Increase the dynamic thresholds slightly to allow for more flexibility in the "C" shapes
    dynamic_threshold_1 = hand_size_1 * 1.5  # For hand 1's "C" shape (relaxed)
    dynamic_threshold_2 = hand_size_2 * 1.5  # For hand 2's "C" shape (relaxed)

    # Check if both hands form "C" shapes (Hand 1 forms a regular "C", Hand 2 forms an opposite "C")
    is_hand1_c_shape = distance_thumb_index_1 < dynamic_threshold_1
    is_hand2_opposite_c_shape = distance_thumb_index_2 < dynamic_threshold_2

    # Check if the thumb tip of Hand 1 is above the index tip of Hand 2 (for "S" shape)
    is_hand1_above_hand2 = thumb_tip_1[1] < index_tip_2[1]  # Smaller Y-coordinate means above

    # Check if thumb of hand 1 and index of hand 2 are close together (relaxed proximity check)
    distance_thumb_1_to_index_2 = np.linalg.norm(thumb_tip_1 - index_tip_2)
    s_shape_threshold = (hand_size_1 + hand_size_2) / 2 * 0.9  # Increased threshold for proximity check

    # Final condition: both hands should form "C" and "opposite C" shapes, thumb of hand 1 touches index of hand 2
    if is_hand1_c_shape and is_hand2_opposite_c_shape and distance_thumb_1_to_index_2 < s_shape_threshold and is_hand1_above_hand2:
        draw_combined_box(image, [landmarks1, landmarks2], "S", color=(0, 255, 0))

        # Optional: Debug visualization of keypoints
        if debug:
            draw_keypoints_for_debugging(image, landmarks1, landmarks2)
        
        return True

    # Optional: Debug visualization even if "S" is not detected
    if debug:
        draw_keypoints_for_debugging(image, landmarks1, landmarks2)

    return False
