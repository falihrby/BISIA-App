import numpy as np
from .common import draw_combined_box, draw_keypoints_for_debugging  # Import both functions

def detect_bisindo_f(landmarks1, landmarks2, image, debug=False):
    # Check if both hands have valid landmarks
    if landmarks1 is None or landmarks2 is None:
        return False

    try:
        # Extract tip landmarks for index and middle fingers of the 1st hand
        index_tip_1 = np.array([landmarks1.landmark[8].x, landmarks1.landmark[8].y])
        middle_tip_1 = np.array([landmarks1.landmark[12].x, landmarks1.landmark[12].y])

        # Calculate distance between the index and middle finger tips for the F shape detection (1st hand)
        distance_index_middle_1 = np.linalg.norm(index_tip_1 - middle_tip_1)

        # Define dynamic threshold based on hand size for proximity between finger tips (1st hand)
        hand_size_1 = np.linalg.norm(index_tip_1 - np.array([landmarks1.landmark[0].x, landmarks1.landmark[0].y]))
        dynamic_threshold_f_1 = hand_size_1 * 0.8  # Adjusted threshold for F detection (1st hand)

        # Check if the index and middle fingers of the 1st hand are close together
        is_fingers_close_1 = distance_index_middle_1 < dynamic_threshold_f_1

        # Extract relevant landmarks for the 2nd hand's index finger tip
        index_tip_2 = np.array([landmarks2.landmark[8].x, landmarks2.landmark[8].y])

        # Extract point 6 (middle finger base) and point 10 (middle finger middle joint) from the 1st hand
        middle_base_1 = np.array([landmarks1.landmark[6].x, landmarks1.landmark[6].y])
        middle_middle_joint_1 = np.array([landmarks1.landmark[10].x, landmarks1.landmark[10].y])

        # Calculate distance between the 2nd hand's index finger tip and points 6 and 10 of the 1st hand
        distance_index_base_2_to_6 = np.linalg.norm(index_tip_2 - middle_base_1)
        distance_index_middle_joint_2_to_10 = np.linalg.norm(index_tip_2 - middle_middle_joint_1)

        # Define dynamic threshold for touching points on the 1st hand
        dynamic_threshold_touch = hand_size_1 * 0.5  # Adjust the threshold for touching detection

        # Check if the index finger of the 2nd hand touches both points 6 and 10 of the 1st hand
        is_touching_1st_hand = (
            distance_index_base_2_to_6 < dynamic_threshold_touch and
            distance_index_middle_joint_2_to_10 < dynamic_threshold_touch
        )

        # Final condition for detecting the letter F
        is_f_shape = is_fingers_close_1 and is_touching_1st_hand

        # If the F shape is detected, draw the bounding box
        if is_f_shape:
            draw_combined_box(image, [landmarks1, landmarks2], "F", color=(0, 255, 0))

            # Optional debug visualization
            if debug:
                draw_keypoints_for_debugging(image, landmarks1)
                draw_keypoints_for_debugging(image, landmarks2)

            return True

        # Optional debug visualization if "F" shape is not detected
        if debug:
            draw_keypoints_for_debugging(image, landmarks1)
            draw_keypoints_for_debugging(image, landmarks2)

        return False

    except Exception:
        return False
