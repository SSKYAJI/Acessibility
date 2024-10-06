import torch
import cv2
import time
import pathlib
import numpy as np

# Modify pathlib to use WindowsPath for compatibility on Windows systems
pathlib.PosixPath = pathlib.WindowsPath

# Load custom-trained YOLOv5 model (update with your model's path)
model = torch.hub.load('ultralytics/yolov5', 'custom', path='Model.pt')


def process_frame(frame):
    """Process the input frame using YOLOv5 model and return the frame with bounding boxes and FPS information."""

    # Start time for FPS calculation
    start_time = time.time()

    # Run inference on the frame using the custom model
    results = model(frame)

    # Render the bounding boxes directly on the frame
    results.render()

    # Calculate FPS (frames per second)
    fps = 1 / (time.time() - start_time)

    # Make a writable copy of the image with bounding boxes
    img_with_boxes = results.ims[0].copy()

    # Add white space at the bottom of the frame for additional info
    height, width, _ = img_with_boxes.shape
    new_height = height + 150  # Extend height for the white space
    img_with_boxes_padded = np.ones((new_height, width, 3), dtype=np.uint8) * 255  # Create white padding
    img_with_boxes_padded[:height, :] = img_with_boxes  # Overlay original image on top

    # Display FPS on the frame
    cv2.putText(img_with_boxes_padded, f'FPS: {fps:.2f}', (10, height + 30),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    # Display detected objects with bounding boxes and information
    for i, box in enumerate(results.xyxy[0]):
        x1, y1, x2, y2, conf, cls_id = map(int, box[:6])
        label = results.names[cls_id]

        # Text format: label, confidence, and bounding box coordinates
        text = f'{label}: {conf:.2f} [{x1}, {y1}, {x2}, {y2}]'
        cv2.putText(img_with_boxes_padded, text, (10, height + 60 + i * 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2)

    # Return processed frame with bounding boxes, FPS, and object information
    return img_with_boxes_padded
