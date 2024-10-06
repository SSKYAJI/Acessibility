import torch

import pathlib
temp = pathlib.PosixPath
pathlib.PosixPath = pathlib.WindowsPath

# Define the path to your weights and input image
weights_path = 'runs/train/exp2/weights/best.pt'
source_image = 'C:\\Users\\usman\\Desktop\\HackathonRepo\\Model\\dataset\\videos\\video-test.mp4'

# Load the model with custom weights
model = torch.hub.load('ultralytics/yolov5', 'custom', path=weights_path)

# Set the confidence threshold and image size
model.conf = 0.9900  # Confidence threshold (0.50)
model.imgsz = 640  # Image size (640)

# Run inference on the source image
results = model(source_image)

# Display the results (bounding boxes, labels, and scores)
results.show()

# Optionally, save the results to an output folder
results.save('output/')
