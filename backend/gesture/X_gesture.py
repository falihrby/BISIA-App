import numpy as np
from .common import draw_combined_box, draw_keypoints_for_debugging

def detect_bisindo_x(landmarks1, landmarks2, image, debug=False):
    if landmarks1 is None or landmarks2 is None:
        return False

    # Get image dimensions
    h, w, _ = image.shape

    # Extract coordinates for the PIP and MCP joints (points 7 and 6) for both hands
    index_pip1 = np.array([landmarks1.landmark[7].x * w, landmarks1.landmark[7].y * h])  # PIP of hand 1
    index_mcp1 = np.array([landmarks1.landmark[6].x * w, landmarks1.landmark[6].y * h])  # MCP of hand 1

    index_pip2 = np.array([landmarks2.landmark[7].x * w, landmarks2.landmark[7].y * h])  # PIP of hand 2
    index_mcp2 = np.array([landmarks2.landmark[6].x * w, landmarks2.landmark[6].y * h])  # MCP of hand 2

    # Calculate dynamic threshold based on hand size (distance from wrist to PIP or MCP)
    wrist1 = np.array([landmarks1.landmark[0].x * w, landmarks1.landmark[0].y * h])
    wrist2 = np.array([landmarks2.landmark[0].x * w, landmarks2.landmark[0].y * h])
    hand_size1 = np.linalg.norm(index_pip1 - wrist1)
    hand_size2 = np.linalg.norm(index_pip2 - wrist2)
    avg_hand_size = (hand_size1 + hand_size2) / 2
    proximity_threshold = avg_hand_size * 0.5  # Set proximity threshold as 20% of the average hand size

    # Check if the PIP or MCP joints are touching (distance is below the threshold)
    distance_pip = np.linalg.norm(index_pip1 - index_pip2)
    distance_mcp = np.linalg.norm(index_mcp1 - index_mcp2)
    are_fingers_touching = distance_pip < proximity_threshold or distance_mcp < proximity_threshold

    # Check if the index fingers are crossing (X-coordinates should be on opposite sides)
    are_fingers_crossing = (index_pip1[0] < index_pip2[0]) or (index_pip1[0] > index_pip2[0])

    # Detect the "X" gesture when fingers are both touching (at points 6 or 7) and crossing
    is_bisindo_x = are_fingers_touching and are_fingers_crossing

    # If the "X" gesture is detected, draw a box around both hands
    if is_bisindo_x:
        draw_combined_box(image, [landmarks1, landmarks2], "X", color=(0, 255, 0))

    # Optional debug visualization
    if debug:
        draw_keypoints_for_debugging(image, landmarks1, landmarks2)

    return is_bisindo_x
