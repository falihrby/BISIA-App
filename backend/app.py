# backend/app.py
from flask import Flask, jsonify, request, Response
from flask_cors import CORS
import cv2
import numpy as np
from handGestureRecognition import process_frame

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return jsonify({"message": "Welcome to BISIA Sign Language Translation API"})

# Video Stream Generator
def generate_frames():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        return jsonify({"error": "Camera is not available"}), 500

    try:
        while True:
            success, frame = cap.read()
            if not success:
                break

            gesture_detected, label, frame = process_frame(frame)
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()

            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    finally:
        cap.release()

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

# Route for gesture detection based on image from frontend
@app.route('/detect-gesture', methods=['POST'])
def detect_gesture():
    if 'frame' not in request.files:
        return jsonify({"error": "No frame provided"}), 400

    file = request.files['frame'].read()
    np_img = np.frombuffer(file, np.uint8)
    frame = cv2.imdecode(np_img, cv2.IMREAD_COLOR)

    gesture_detected, label, processed_frame = process_frame(frame)

    # Draw the landmarks on the processed frame before sending it back
    _, buffer = cv2.imencode('.jpg', processed_frame)
    frame_encoded = buffer.tobytes()

    if gesture_detected:
        return Response(frame_encoded, mimetype='image/jpeg'), 200
    else:
        return Response(frame_encoded, mimetype='image/jpeg'), 200

if __name__ == '__main__':
    app.run(debug=True)
