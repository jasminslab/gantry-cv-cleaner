# Computer Vision for Guinea Pig Droppings Detection
This module contains the core image pre-processing logic and the computer vision algorithms.


## Data Processing Steps

**1. Extract Images from Video:**
First, extract frames from the videos using the following script:

```bash
python software/computer_vision/data_processing/video_to_image.py
```

**2. Label Images:** 
Use the *lableme* tool to annotate the images.

```bash
lableme
```

Note: This will create json file per image.

**3. Convert Labels for yolo:** the yolo model requires annotations in a .txt format.
Convert the json files using:

```bash
python software/computer_vision/data_processing/convert_json_to_txt.py
```




