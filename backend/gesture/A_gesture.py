import numpy as np
from .common import draw_combined_box, draw_keypoints_for_debugging  # Import both functions

def detect_bisindo_a(landmarks1, landmarks2, image, debug=False):
    if landmarks1 is None or landmarks2 is None:
        return False
    
    # Extract landmarks for thumbs and index fingers (both hands)
    thumb_tip1 = np.array([landmarks1.landmark[4].x, landmarks1.landmark[4].y])
    index_tip1 = np.array([landmarks1.landmark[8].x, landmarks1.landmark[8].y])
    thumb_tip2 = np.array([landmarks2.landmark[4].x, landmarks2.landmark[4].y])
    index_tip2 = np.array([landmarks2.landmark[8].x, landmarks2.landmark[8].y])

    # Calculate distances between corresponding fingertips
    distance_index_fingers = np.linalg.norm(index_tip1 - index_tip2)
    distance_thumbs = np.linalg.norm(thumb_tip1 - thumb_tip2)
    
    # Dynamic threshold based on hand size
    hand_size1 = np.linalg.norm(index_tip1 - thumb_tip1)
    hand_size2 = np.linalg.norm(index_tip2 - thumb_tip2)
    dynamic_threshold = (hand_size1 + hand_size2) / 2 * 0.4  # Adjust threshold

    # Check if the index fingers and thumbs are close enough
    are_index_fingers_close = distance_index_fingers < dynamic_threshold
    are_thumbs_close = distance_thumbs < dynamic_threshold
    
    # Additional checks to ensure other fingers are not extended (folded)
    def fingers_folded(landmarks):
        return all(landmarks.landmark[i].y > landmarks.landmark[i - 2].y for i in [12, 16, 20])

    are_other_fingers_folded = fingers_folded(landmarks1) and fingers_folded(landmarks2)

    # Detect the gesture
    is_bisindo_a = are_index_fingers_close and are_thumbs_close and are_other_fingers_folded

    if is_bisindo_a:
        draw_combined_box(image, [landmarks1, landmarks2], "A", color=(0, 255, 0))

    # Optional Debug Visualization using the helper function
    if debug:
        draw_keypoints_for_debugging(image, landmarks1, landmarks2)

    return is_bisindo_a
