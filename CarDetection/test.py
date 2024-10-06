import torch
import cv2
import time

# Load the pre-trained YOLOv5s model into memory (only once)
model = torch.hub.load('ultralytics/yolov5', 'yolov5s')

def process_image(img_path):
    # Measure the time taken for the process
    start_time = time.time()

    # Read the image
    img = cv2.imread(img_path)

    # Run inference on the processed image
    results = model(img)

    # Measure end time for inference
    end_time = time.time()
    inference_time = end_time - start_time
    print(f"Inference time: {inference_time:.4f} seconds")

    # Extract detected objects' details (coordinates, labels, confidence scores)
    df = results.pandas().xyxy[0]  # Get the results as a DataFrame

    # Filter for cars (assuming class ID 2 corresponds to 'car')
    print(df)
    car_coordinates = df[df['name'] == 'car'][['xmin', 'ymin', 'xmax', 'ymax', 'confidence']]

    # Print car coordinates and confidence scores
    print("Detected car coordinates:")
    print(car_coordinates)

    # Return car coordinates if needed
    return car_coordinates

# Example usage
img_path = 'Sample.png'  # Replace with the path to your image

# Test the inference
process_image(img_path)