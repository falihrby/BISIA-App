import cv2
import mediapipe as mp

# Function to visualize hand landmarks on webcam
def visualize_hand_landmarks():
    # Initialize mediapipe hands model
    mp_hands = mp.solutions.hands
    mp_drawing = mp.solutions.drawing_utils
    hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)

    # Initialize webcam feed
    cap = cv2.VideoCapture(0)

    while cap.isOpened():
        success, image = cap.read()
        if not success:
            print("Ignoring empty camera frame.")
            continue

        # Flip the image horizontally and convert the color space from BGR to RGB
        image = cv2.flip(image, 1)
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # Process the image and find hands
        results = hands.process(image_rgb)

        # If hands are found
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                # Draw landmarks and connections on the image
                mp_drawing.draw_landmarks(
                    image, 
                    hand_landmarks, 
                    mp_hands.HAND_CONNECTIONS,
                    mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=4),  # Green landmarks
                    mp_drawing.DrawingSpec(color=(255, 0, 0), thickness=2)  # Blue connections
                )

        # Show the image with landmarks
        cv2.imshow('Hand Landmarks', image)

        # Break loop if 'q' is pressed
        if cv2.waitKey(5) & 0xFF == ord('q'):
            break

    # Release the webcam and close the window
    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    visualize_hand_landmarks()
