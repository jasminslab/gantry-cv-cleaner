import cv2
import os

# Configuration
video_folder_path = 'data/cv_dataset/raw_videos'
output_dir = 'data/cv_dataset/images' 
frame_rate = 30
os.makedirs(output_dir, exist_ok=True)

# List all files in the directory
video_files = [video for video in os.listdir(video_folder_path) if video.lower().endswith(('.mp4'))]

if not video_files:
    print(f"No video files found in {video_folder_path}")
else:
    print(f"Found {len(video_files)} videos. Starting processing...")

total_saved_count = 0


for video_file in video_files:
    full_video_path = os.path.join(video_folder_path, video_file)    
    
    cap = cv2.VideoCapture(full_video_path)
    
    if not cap.isOpened():
        print(f"Error opening video file {video_file}")
        continue

    frame_count = 0
    saved_count_per_video = 0
    
    video_name_stem = os.path.splitext(video_file)[0]

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        
        # Saves every n-th frame 
        if frame_count % frame_rate == 0:
            # Construct filename
            filename = f"{video_name_stem}_frame_{saved_count_per_video:05d}.jpg"
            output_path = os.path.join(output_dir, filename)
            
            cv2.imwrite(output_path, frame)
            
            saved_count_per_video += 1
            total_saved_count += 1
        
        frame_count += 1

    cap.release()
    print(f"Finished {video_file}: Saved {saved_count_per_video} images.")

cv2.destroyAllWindows()
print(f"Processing completed")