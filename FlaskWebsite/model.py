import torch
import cv2
import time
import pathlib
import numpy as np

temp = pathlib.PosixPath
pathlib.PosixPath = pathlib.WindowsPath

# Load your custom-trained YOLOv5 model (replace the path with your model's path)
model = torch.hub.load('ultralytics/yolov5', 'custom', path='exp30/weights/best.pt')

def process_frame(frame):
    # Start time for FPS calculation
    start_time = time.time()
    #frame = cv2.resize(frame, (416))
    #frame = cv2.resize(frame, (width // 2, height // 2))
    # Run inference on the frame using the custom model
    results = model(frame)

    # Use the built-in render() function to draw the boxes automatically
    results.render()  # This modifies the frame in-place with bounding boxes

    # Calculate FPS (frames per second)
    end_time = time.time()
    fps = 1 / (end_time - start_time)

    # Make a writable copy of the image (convert from read-only)
    img_with_boxes = results.ims[0].copy()

    # Add white space at the bottom of the frame
    height, width, _ = img_with_boxes.shape
    new_height = height + 150  # Increase the height to add white space
    img_with_boxes_padded = np.ones((new_height, width, 3), dtype=np.uint8) * 255  # Create a white image
    img_with_boxes_padded[:height, :] = img_with_boxes  # Place the original image in the top part

    # Draw the FPS on the frame in the new padded space
    cv2.putText(img_with_boxes_padded, f'FPS: {fps:.2f}', (10, height + 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    # Display detected objects and their information
    for i, (label, confidence, box) in enumerate(zip(results.names, results.xyxy[0][:, -1], results.xyxy[0])):
        x1, y1, x2, y2 = map(int, box[:4])  # Get bounding box coordinates
        conf = box[4]  # Confidence score

        # Write object information below the frame
        text = f'{label}: {conf:.2f} [{x1}, {y1}, {x2}, {y2}]'
        cv2.putText(img_with_boxes_padded, text, (10, height + 60 + i * 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2)

    # Return the processed frame with bounding boxes, FPS, and object information
    return img_with_boxes_padded
