# PARKhub - HackSMU Project
## Judah Boyce, Shashank Yaji, Usman Khan, and Tejaswi Kulkarni

## Folder Directory
- .archive - This contains old files not required for the presentation. 
- CarDetection - This contains tests we conducted utilizing a public general YOLOv5 model. This model could detect cars, but could not detect the accessibility sign. This model appeared to be too slow, prompting us to train our own car model. 
- DatasetManipulation - Code for manipulating images to create larger datasets. Actual dataset not included. Resizes, colors, and distorts images.
- FlaskWebsite - The current complete website. Contains front end and backend, including our best model. 
- OpenCV - Reference code for manipulating videos frame by frame which was used when writing the FlaskWebsite code

## Inspiration
We were inspired by the challenging parking situations faced with accessibility needs when finding available parking. We wanted to create a solution that provides real time help to those 

## What it does
Our app helps people find accessible parking spots easily. It uses AI to watch parking areas and spot open spaces in real time. The app guides users to these spots, making parking faster. It shows live updates on available spaces and uses easy-to-read maps. We've made the app simple to use, with a design inspired by ParkHub. Our system uses YOLO-v5 to detect cars and accessibility symbols, working at 6-15 FPS with 50-70% accuracy. By making it easier to find accessible parking, our app improves parking for people with disabilities in busy areas.

## How we built it
We built our accessibility parking solution through several key steps:

Data Collection: Web scraping, AI image generation, and manual collection of 200 photos from SMU campus.
Preprocessing: Used "Make Sense AI" to map and label datasets.
Model Training: Employed YOLOv5 to train a custom model recognizing cars and accessibility symbols.
Backend Development: Implemented a multi-threaded preprocessing pipeline with OpenCV, including frame resizing for efficiency.
Frontend Integration: Developed a Flask-based frontend with a real-time statistics dashboard.
Optimization: Focused on video compression, multithreading, and increasing epochs for improved accuracy.

Our model achieved 50-70% confidence scores, 6-15 FPS, and 35-60ms response times. We trained on 800 images over 4 hours, reaching 14 epochs. The UI was inspired by the ParkHub app for real-world alignment.

## Challenges we ran into
There were many challenges we overcame while building Acessibility. To begin, during our research we realized there was a limited amount of public datasets containing the icon of accessibility. This prompted us to create our own dataset, through scraping images, modifying them to create multiple versions, and collecting our own data by taking images around the SMU campus.  

## Accomplishments that we're proud of
Achieved high model performance: 50-70% confidence scores, 6-15 FPS, and 35-60ms response times.
Efficient training: 800 images processed in 4 hours, reaching 14 epochs.
Real-world application: Collected 200 campus photos and designed UI inspired by ParkHub.
Innovative technical implementation: Multi-threaded preprocessing, custom YOLO-v5 model, and OpenCV integration.
Effective optimization: Video compression, multithreading, and frame resizing for improved speed.

## What we learned
Through this project, we learned a lot about using AI for real-world problems, especially in accessibility. We faced challenges in data collection, model training, and balancing speed with accuracy. We gained practical skills in video processing and web development. Most importantly, we realized how much more there is to learn about creating truly helpful technology for people with disabilities. This experience showed us the potential of AI in improving accessibility, while also humbling us with the complexity of the task.

## What's next for Acessibility 
Expand dataset and improve model accuracy for better detection in various conditions.
Develop a user-friendly mobile app with real-time updates from multiple parking locations.
Partner with local businesses and events to provide specialized accessibility information and wider coverage.
