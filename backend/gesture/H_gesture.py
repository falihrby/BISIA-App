import numpy as np
from .common import draw_combined_box, draw_keypoints_for_debugging  # Import both functions

def detect_bisindo_h(landmarks1, landmarks2, image, debug=False):
    if landmarks1 is None or landmarks2 is None:
        return False

    try:
        # Extract point 12 (middle finger tip) from the 1st hand and point 6 (middle finger base) from the 2nd hand
        point_12_1 = np.array([landmarks1.landmark[12].x, landmarks1.landmark[12].y])
        point_6_2 = np.array([landmarks2.landmark[6].x, landmarks2.landmark[6].y])

        # Calculate the distance between point 12 of the 1st hand and point 6 of the 2nd hand
        distance_12_6 = np.linalg.norm(point_12_1 - point_6_2)

        # Dynamic threshold based on the size of the hands (average hand size)
        hand_size_1 = np.linalg.norm(point_12_1 - np.array([landmarks1.landmark[0].x, landmarks1.landmark[0].y]))
        hand_size_2 = np.linalg.norm(point_6_2 - np.array([landmarks2.landmark[0].x, landmarks2.landmark[0].y]))
        dynamic_threshold = (hand_size_1 + hand_size_2) / 2 * 0.5  # Adjust threshold for detection

        # Check if the middle finger tip of the 1st hand is close to the middle finger base of the 2nd hand
        is_touching = distance_12_6 < dynamic_threshold

        # Check if the index fingers of both hands are in a "standing" position
        is_index_standing_1 = landmarks1.landmark[8].y < landmarks1.landmark[5].y  # 1st hand index finger standing
        is_index_standing_2 = landmarks2.landmark[8].y < landmarks2.landmark[5].y  # 2nd hand index finger standing

        # Final condition for detecting the letter H
        is_h_shape = is_touching and is_index_standing_1 and is_index_standing_2

        # If the "H" gesture is detected, draw the bounding box
        if is_h_shape:
            draw_combined_box(image, [landmarks1, landmarks2], "H", color=(0, 255, 0))

            # Optional debug visualization
            if debug:
                draw_keypoints_for_debugging(image, landmarks1)
                draw_keypoints_for_debugging(image, landmarks2)

            return True

        # Optional debug visualization if "H" shape is not detected
        if debug:
            draw_keypoints_for_debugging(image, landmarks1)
            draw_keypoints_for_debugging(image, landmarks2)

        return False

    except Exception:
        return False
