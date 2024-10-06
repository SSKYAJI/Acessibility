from flask import Flask, render_template, request, Response, jsonify
import cv2
import os
from model import process_frame

app = Flask(__name__)
UPLOAD_FOLDER = 'static/uploaded_videos'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


# Home page with upload form
@app.route('/')
def index():
    return render_template('index.html')

app.route('/about')
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
    while video.isOpened():
        success, frame = video.read()
        if not success:
            break
        # Process the frame through the AI model
        height, width, channels = frame.shape

        frame = cv2.resize(frame, (width // 4, height // 4))
        frame = process_frame(frame)
        # Encode the frame in JPEG format
        _, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        # Yield the frame for streaming
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    video.release()


if __name__ == '__main__':
    app.run(debug=True)
