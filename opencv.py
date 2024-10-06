import cv2
import time
import numpy as np
from threading import Thread
from queue import Queue

# Placeholder for ML model
class DummyModel:
    def predict(self, frame):
        # This is where your actual ML model will make predictions
        # For now, it just returns a dummy bounding box

        return [{"bbox": [10, 10, 100, 100], "confidence": 0.95}]

class VideoProcessor:
    def __init__(self, video_source=0):
        self.capture = cv2.VideoCapture(video_source)
        self.frame_queue = Queue(maxsize=128)
        self.result_queue = Queue(maxsize=128)
        self.model = DummyModel()
        self.stopped = False

    def start(self):

        Thread(target=self.update, args=()).start()
        Thread(target=self.process_frames, args=()).start()
        return self

    def update(self):
        while True:
            if self.stopped:
                return
            if not self.frame_queue.full():
                ret, frame = self.capture.read()
                if not ret:
                    self.stop()
                    return
                self.frame_queue.put(frame)

    def preprocess_frame(self, frame):
        # Implement your preprocessing here
        # For example, resize the frame
        return cv2.resize(frame, (416, 416))

    def process_frames(self):

        while True:
            if self.stopped:
                return
            if not self.frame_queue.empty():
                frame = self.frame_queue.get()
                processed_frame = self.preprocess_frame(frame)
                
                start_time = time.time()
                
                # Run model prediction
                results = self.model.predict(processed_frame)
                
                # Post-process results (draw bounding boxes, etc.)
                for result in results:
                    bbox = result['bbox']
                    conf = result['confidence']
                    cv2.rectangle(frame, (bbox[0], bbox[1]), (bbox[2], bbox[3]), (0, 255, 0), 2)
                    cv2.putText(frame, f"{conf:.2f}", (bbox[0], bbox[1]-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0,255,0), 2)
                
                process_time = (time.time() - start_time) * 1000  # Convert to ms
                cv2.putText(frame, f"Process time: {process_time:.2f}ms", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)
                
                self.result_queue.put(frame)

    def read(self):
        return self.result_queue.get()

    def stop(self):
        self.stopped = True

def main():
    video_processor = VideoProcessor(0).start()  # 0 for webcam, or provide video file path
    
    while True:
        frame = video_processor.read()
        cv2.imshow("Frame", frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    video_processor.stop()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()