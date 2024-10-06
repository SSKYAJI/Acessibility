import cv2
import time
import numpy as np
from threading import Thread
from queue import Queue


# Dummy ML model class for reference
class DummyModel:
    def predict(self, frame):
        """
        Placeholder for model prediction.
        Replace this with actual ML model inference.
        """
        # Returns a dummy bounding box with confidence
        return [{"bbox": [10, 10, 100, 100], "confidence": 0.95}]


# Video processing pipeline
class VideoProcessor:
    def __init__(self, video_source=0):
        """
        Initializes video capture and sets up frame/result queues.
        Uses DummyModel for predictions.
        """
        self.capture = cv2.VideoCapture(video_source)  # Video source (0 for webcam)
        self.frame_queue = Queue(maxsize=128)  # Queue for storing frames
        self.result_queue = Queue(maxsize=128)  # Queue for processed frames (with results)
        self.model = DummyModel()  # ML model (can replace with real model)
        self.stopped = False  # Flag to stop threads

    def start(self):
        """
        Starts threads for reading frames and processing them.
        """
        Thread(target=self.update, args=()).start()  # Thread for capturing frames
        Thread(target=self.process_frames, args=()).start()  # Thread for processing frames
        return self

    def update(self):
        """
        Reads frames from the video source and adds them to the frame queue.
        """
        while True:
            if self.stopped:
                return
            if not self.frame_queue.full():  # Check if queue is full
                ret, frame = self.capture.read()  # Capture a frame
                if not ret:  # If no frame captured, stop processing
                    self.stop()
                    return
                self.frame_queue.put(frame)  # Add frame to the queue

    def preprocess_frame(self, frame):
        """
        Preprocesses the frame (e.g., resizing) before passing it to the model.
        """
        # Resize frame to a fixed size for model input
        return cv2.resize(frame, (416, 416))

    def process_frames(self):
        """
        Processes frames from the frame queue using the ML model,
        draws bounding boxes, and stores the results in the result queue.
        """
        while True:
            if self.stopped:
                return
            if not self.frame_queue.empty():
                frame = self.frame_queue.get()  # Get a frame from the queue
                processed_frame = self.preprocess_frame(frame)  # Preprocess the frame

                start_time = time.time()  # Start time for performance measurement

                # Run model prediction on the preprocessed frame
                results = self.model.predict(processed_frame)

                # Draw bounding boxes and add confidence score to the frame
                for result in results:
                    bbox = result['bbox']
                    conf = result['confidence']
                    cv2.rectangle(frame, (bbox[0], bbox[1]), (bbox[2], bbox[3]), (0, 255, 0), 2)
                    cv2.putText(frame, f"{conf:.2f}", (bbox[0], bbox[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9,
                                (0, 255, 0), 2)

                process_time = (time.time() - start_time) * 1000  # Calculate processing time in milliseconds
                cv2.putText(frame, f"Process time: {process_time:.2f}ms", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1,
                            (0, 0, 255), 2)

                self.result_queue.put(frame)  # Store the processed frame in the result queue

    def read(self):
        """
        Reads the processed frame from the result queue.
        """
        return self.result_queue.get()

    def stop(self):
        """
        Stops the video processing and releases resources.
        """
        self.stopped = True


# Main function to run video processing
def main():
    video_processor = VideoProcessor(0).start()  # Start video processing (0 for webcam)

    while True:
        frame = video_processor.read()  # Get the processed frame
        cv2.imshow("Frame", frame)  # Display the frame

        if cv2.waitKey(1) & 0xFF == ord('q'):  # Break the loop if 'q' is pressed
            break

    video_processor.stop()  # Stop the video processor
    cv2.destroyAllWindows()  # Close all OpenCV windows


# Entry point of the script
if __name__ == "__main__":
    main()
