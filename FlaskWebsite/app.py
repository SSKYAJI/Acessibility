from flask import Flask, render_template, request, Response, jsonify
import cv2
import os
import time
import numpy as np
from model import process_frame

app = Flask(__name__)
UPLOAD_FOLDER = 'static/uploaded_videos'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Home page with upload form
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

# Route to handle video upload via AJAX
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file:
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)
        return jsonify({'filename': file.filename}), 200

# Route to stream video frame by frame
@app.route('/video_feed/<filename>')
def video_feed(filename):
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    return Response(generate_frames(filepath), mimetype='multipart/x-mixed-replace; boundary=frame')

# Function to generate video frames for streaming
def generate_frames(filepath):
    video = cv2.VideoCapture(filepath)
    fps = video.get(cv2.CAP_PROP_FPS)  # Get the FPS of the video
    prev_frame = None  # Initialize previous frame for comparison
    threshold = 1  # Set threshold for frame difference

    while video.isOpened():
        start_time = time.time()  # Track frame processing time
        success, frame = video.read()
        if not success:
            break

        # Convert frame to grayscale for easier comparison
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        if prev_frame is not None:
            # Calculate absolute difference between current and previous frames
            frame_diff = cv2.absdiff(prev_frame, gray_frame)
            diff_mean = np.mean(frame_diff)

            # Only process the frame if the difference exceeds the threshold
            if diff_mean > threshold:
                frame = process_frame(frame)
            else:
                print(f"Skipped frame with diff mean: {diff_mean}")
        else:
            # Process the first frame without comparison
            frame = process_frame(frame)

        prev_frame = gray_frame  # Update previous frame

        # Encode the frame in JPEG format
        _, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()

        # Yield the frame for streaming
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

        # Control playback speed dynamically based on processing time
        elapsed_time = time.time() - start_time
        delay = max(1 / fps - elapsed_time, 0)  # Ensure non-negative delay
        time.sleep(delay)

    video.release()

if __name__ == '__main__':
    app.run(debug=True)
