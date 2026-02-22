from ultralytics import YOLO
import os

# Relevant Paths
model_path = 'runs/detect/poops_v203/weights/best.pt' 
source_images_dir = 'data/cv_dataset/raw_images_test'

# Load trained model
try:
    model = YOLO(model_path)
except Exception as e:
    print(f"Error: Model coun't be loaded from: {model_path}")
    print(e)
    exit()

print(f"Start prediction calculation (Path to model: {model_path} )")
results = model.predict(
    source=source_images_dir, 
    save=True, 
    conf=0.25
)

print("Prediction completed")
print(f"Annoted pictures saved here: {results[0].save_dir}")