import os
import json
from tqdm import tqdm

def convert_annotation(json_file_path, output_dir, class_list):
    """
    This function converts annotations stored in json format to txt format.

    json_file_path: path to the json file
    output_dir: path to target folder for txt files
    class list: list of lable names
    """

    try:
        with open(json_file_path, 'r') as f:
            data = json.load(f)

        w = data.get('imageWidth')
        h = data.get('imageHeight')

        if not w or not h:
            print(f"Invalid image size: {json_file_path}")
            return

        basename = os.path.basename(json_file_path).replace('.json', '')
        out_file_path = os.path.join(output_dir, basename + '.txt')
        
        with open(out_file_path, 'w') as out_file:
            for shape in data.get('shapes', []):
                cls_name = shape.get('label')
                
                if cls_name not in class_list:
                    continue
                
                cls_id = class_list.index(cls_name)
                points = shape.get('points')
                
                x_coords = [p[0] for p in points]
                y_coords = [p[1] for p in points]
                xmin = min(x_coords)
                xmax = max(x_coords)
                ymin = min(y_coords)
                ymax = max(y_coords)
                
                # yolo formatting
                b = (float(xmin), float(xmax), float(ymin), float(ymax))
                bb = convert_bbox((w, h), b)
                
                out_file.write(str(cls_id) + " " + " ".join([f"{a:.6f}" for a in bb]) + '\n')

    except Exception as e:
        print(f"Error detected in the following file: {json_file_path}, {e}")

def convert_bbox(size, box):
    """
    This function converts box coordinates from absolute pixel values to a normalizes yolo format
    """
    dw = 1. / size[0]
    dh = 1. / size[1]
    x = (box[0] + box[1]) / 2.0
    y = (box[2] + box[3]) / 2.0
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x * dw
    y = y * dh
    w = w * dw
    h = h * dh
    return (x, y, w, h)

if __name__ == "__main__":
    CLASSES = ["Poops"] 
    RAW_DATA_DIR = 'data/cv_dataset/images' 
    YOLO_LABELS_DIR = 'data/cv_dataset/labels'

    os.makedirs(YOLO_LABELS_DIR, exist_ok=True)

    if not os.path.exists(RAW_DATA_DIR):
        print(f"No folder found: {RAW_DATA_DIR}")
    else:
        json_files = [file for file in os.listdir(RAW_DATA_DIR) if file.endswith('.json')]

        if not json_files:
            print(f"No json file found: {RAW_DATA_DIR}")
        else:            
            for json_file in tqdm(json_files):
                json_path = os.path.join(RAW_DATA_DIR, json_file)
                convert_annotation(json_path, YOLO_LABELS_DIR, CLASSES)

            print("Conversion completed!")