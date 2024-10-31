import cv2
import numpy as np

def enhance_video(input_path, output_path, brightness=0, contrast=1):
    # Open the video
    cap = cv2.VideoCapture(input_path)
    
    # Get video properties
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    
    # Create VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        
        # Adjust brightness and contrast
        adjusted = cv2.convertScaleAbs(frame, alpha=contrast, beta=brightness)
        
        # Write the frame
        out.write(adjusted)
    
    # Release everything
    cap.release()
    out.release()
    cv2.destroyAllWindows()

# Usage
enhance_video('/Users/blackhole/Downloads/VID_20240902_234235.mp4', 'output_video.mp4', brightness=50, contrast=1.5)