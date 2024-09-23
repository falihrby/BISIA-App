from flask import Flask, jsonify, Response
import cv2
from handGestureRecognition import process_frame

app = Flask(__name__)

# Home route
@app.route('/')
def home():
    return jsonify({"message": "Welcome to BISIA Sign Language Translation API"})

# Video Stream Generator
def generate_frames():
    cap = cv2.VideoCapture(0)
    while True:
        success, frame = cap.read()
        if not success:
            break
        else:
            gesture_detected, label, frame = process_frame(frame)
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()

            # Yield the frame as a response to the client
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    cap.release()

# Route for video stream
@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

# Route for detecting a gesture
@app.route('/translate', methods=['GET'])
def translate():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        return jsonify({"error": "Camera not available"}), 500

    gesture_detected = False
    label = None
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Call the gesture detection function
        gesture_detected, label, frame = process_frame(frame)

        # Break when a gesture is detected
        if gesture_detected:
            break

    cap.release()
    return jsonify({"message": f"Gesture detected: {label}"}), 200

if __name__ == '__main__':
    app.run(debug=True)
