import time
import cv2
import os
import numpy as np
from mss import mss
from PIL import Image

# Function to capture the screen
def capture_screen():
    with mss() as sct:
        monitor = sct.monitors[0]  # Get the principal monitor
        sct_img = sct.grab(monitor)
        img = Image.frombytes("RGB", sct_img.size, sct_img.bgra, "raw", "BGRX")
        return np.array(img)

# Function to delete the N oldest images from the directory
def delete_oldest_images(directory, n):
    sorted_images = sorted(os.listdir(directory), key=lambda x: os.path.getctime(os.path.join(directory, x)))
    for i in range(min(n, len(sorted_images))):
        try:
            os.remove(os.path.join(directory, sorted_images[i]))
        except Exception as e:
            print(f"Error deleting image: {e}")

# Create the temp/img directory if it doesn't exist
os.makedirs("temp/img", exist_ok=True)

# Capture frames at 10 FPS
fps = 1
frame_counter = 0
while True:
    start_time = time.time()
    
    frame = capture_screen()
    frame_path = f"temp/img/frame_{frame_counter:06d}.jpg"
    cv2.imwrite(frame_path, cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))
    frame_counter += 1

    # Process the frame here, for example, call process_image() with the captured frame

    if frame_counter%100 == 0:
        delete_oldest_images("temp/img", 50)
        #frame_counter = 50  # Reset the counter to 500, as 500 images are still remaining

    # Wait for the next frame
    time.sleep(max(1./fps - (time.time() - start_time), 0))