import numpy as np
from .common import draw_combined_box, draw_keypoints_for_debugging  # Import both functions

def detect_bisindo_k(landmarks1, landmarks2, image, debug=False):
    if landmarks1 is None or landmarks2 is None:
        return False

    # Extract the landmarks for point 6 (MCP of index finger) on both hands
    point6_hand1 = np.array([landmarks1.landmark[6].x, landmarks1.landmark[6].y])
    point6_hand2 = np.array([landmarks2.landmark[6].x, landmarks2.landmark[6].y])

    # Calculate the distance between point 6 on both hands
    distance_between_6 = np.linalg.norm(point6_hand1 - point6_hand2)

    # Dynamic threshold based on hand size (average hand size between both hands)
    hand_size1 = np.linalg.norm(
        np.array([landmarks1.landmark[0].x, landmarks1.landmark[0].y]) - 
        np.array([landmarks1.landmark[9].x, landmarks1.landmark[9].y])
    )
    hand_size2 = np.linalg.norm(
        np.array([landmarks2.landmark[0].x, landmarks2.landmark[0].y]) - 
        np.array([landmarks2.landmark[9].x, landmarks2.landmark[9].y])
    )
    average_hand_size = (hand_size1 + hand_size2) / 2

    # Adjust dynamic threshold based on the sensitivity you need
    dynamic_threshold = average_hand_size * 0.5  # Adjust threshold for sensitivity

    # Check if point 6 on both hands are close enough to touch
    is_touching = distance_between_6 < dynamic_threshold

    # Final condition for detecting the letter "K"
    if is_touching:
        draw_combined_box(image, [landmarks1, landmarks2], "K", color=(0, 255, 0))

        # Optional: Debug visualization of keypoints
        if debug:
            draw_keypoints_for_debugging(image, landmarks1, landmarks2)
        
        return True
    else:
        # Optional: Debug visualization even when the shape is not detected
        if debug:
            draw_keypoints_for_debugging(image, landmarks1, landmarks2)

        return False
