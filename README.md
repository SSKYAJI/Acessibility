# PARKhub - HackSMU Project

## Folder Directory
- DatasetManipulation - Code for manipulating images to create larger datasets. Actual dataset not included, it'll be sent in the discord group. 
- Model - This is the main Model for our code. To add more data, add it in the dataset folder. The following commands is mostly all you'll need: 
  - so for training the model  python train.py --img 640 --batch 16 --epochs 1 --data data/custom.yaml --weights yolov5s.pt --cache
  - for inference.  python detect.py --weights runs/train/exp2/weights/best.pt --source dataset/videos/video-test.mp4 --img 640 --conf 0.10
  - make sure that the files paths are mathcing to your project requriements
- .venv - This has the files for all the of dependencies, it is quite large