import numpy as np
from .common import draw_combined_box, draw_keypoints_for_debugging  # Import both functions

def detect_bisindo_g(landmarks1, landmarks2, image, debug=False):
    if landmarks1 is None or landmarks2 is None:
        return False

    # Check if fingers are closed by comparing tip and base positions
    def is_hand_clenched(landmarks):
        tips = [landmarks.landmark[i].x for i in [4, 8, 12, 16, 20]]  # Finger tips
        bases = [landmarks.landmark[i].x for i in [3, 5, 9, 13, 17]]  # Finger bases
        closed_count = sum(np.linalg.norm(np.array(tips[i]) - np.array(bases[i])) < 0.05 for i in range(5))  # 80% closed fingers
        return closed_count >= 3

    # Check if both hands are clenched
    hand1_clenched = is_hand_clenched(landmarks1)
    hand2_clenched = is_hand_clenched(landmarks2)

    # Calculate distance between wrists and define dynamic threshold based on hand size
    distance_between_hands = np.linalg.norm(
        np.array([landmarks1.landmark[0].x, landmarks1.landmark[0].y]) - 
        np.array([landmarks2.landmark[0].x, landmarks2.landmark[0].y])
    )
    hand_size = np.linalg.norm(
        np.array([landmarks1.landmark[0].x, landmarks1.landmark[0].y]) - 
        np.array([landmarks1.landmark[9].x, landmarks1.landmark[9].y])
    )
    dynamic_threshold_g = hand_size * 2

    # Check if both hands are clenched and close to each other
    if hand1_clenched and hand2_clenched and distance_between_hands < dynamic_threshold_g:
        draw_combined_box(image, [landmarks1, landmarks2], "G", color=(0, 255, 0))

        # Optional debug visualization
        if debug:
            draw_keypoints_for_debugging(image, landmarks1, landmarks2)

        return True

    # Optional debug visualization if "G" shape is not detected
    if debug:
        draw_keypoints_for_debugging(image, landmarks1, landmarks2)

    return False
