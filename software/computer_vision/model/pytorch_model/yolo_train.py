import torch
from ultralytics import YOLO
import os
#import glob
#import cv2
import matplotlib.pyplot as plt
import yaml

# Path configurations
PROJECT_ROOT = os.path.abspath(os.getcwd())
BASE_DATA_PATH = os.path.join(PROJECT_ROOT, 'data/cv_dataset')

IMG_DIR_NAME = 'images'
LABEL_DIR_NAME = 'labels'

YAML_FILE = os.path.join(PROJECT_ROOT, 'software/computer_vision/model/poops.yaml')
MODEL_PATH = os.path.join(PROJECT_ROOT, 'software/computer_vision/model/pytorch_model/yolov8n.pt')
RUN_NAME = 'poops_v20'

def create_yaml():
    """Creation of poops.yaml"""

    yaml_content = {
        'path': os.path.abspath(BASE_DATA_PATH), 
        'train': IMG_DIR_NAME, 
        'val': IMG_DIR_NAME,
        'names': {
            0: 'Poops'
        }
    }

    # Check if targed folder exists
    os.makedirs(os.path.dirname(YAML_FILE), exist_ok=True)

    with open(YAML_FILE, 'w') as f:
        yaml.dump(yaml_content, f, default_flow_style=False)

def main():
    create_yaml()

    # Load model
    if not os.path.exists(MODEL_PATH):
        print(f"Error: Model not found: {MODEL_PATH}")
        model = 'yolov8s.pt'
        

    print(f"Load Model from: {MODEL_PATH}...")
    model = YOLO(MODEL_PATH)

    # Start training ...
    device = 0 if torch.cuda.is_available() else 'cpu'
    
    print("Start training ...")
    model.train(
        data=os.path.abspath(YAML_FILE),
        epochs=100,
        imgsz=1280,
        batch=3,
        name=RUN_NAME,
        device=device,
        #patience=10,
        #exist_ok=True,
        #optimizer='AdamW',
        #lr0=0.001,
        #lrf=0.01,
        #mosaic=0.0,
        #close_mosaic=0, 
        #scale=0.1,
    )

if __name__ == '__main__':
    main()