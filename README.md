# Accessibility Parking Finder

## About The Project
This project aims to improve accessibility parking for users with disabilities. Using AI and computer vision, we've developed a system that detects and tracks the availability of accessible parking spaces in real-time.

### Key Features:
- Real-time detection of cars and accessibility symbols
- Dynamic routing to available accessible parking spots
- User-friendly interface inspired by ParkHub

## Tech Stack
- AI Model: YOLO-v5
- Backend: OpenCV, Flask
- Frontend: Flask templates, JavaScript

## Performance
- Confidence Score: 50-70%
- FPS Achieved: 6-15 fps
- Response Time: 35-60ms
- Dataset size: 800 images

## Installation

### Prerequisites

- Python 3.7+
- pip

### Required Libraries

```
opencv-python
numpy
torch
flask
```

### Installation Steps

1. Clone the repository
   ```
   git clone https://github.com/yourusername/your-repo-name.git
   cd your-repo-name
   ```

2. Create a virtual environment (optional but recommended)
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install required libraries
   ```
   pip install -r requirements.txt
   ```

4. Run the application
   ```
   python app.py
   ```

5. Open a web browser and go to `http://localhost:5000`

## Future Plans

1. Expand dataset and improve model accuracy
2. Develop a user-friendly mobile app
3. Partner with local businesses for wider coverage

## Acknowledgments

- SMU Campus for data collection
- ParkHub for UI inspiration
