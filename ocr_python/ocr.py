import cv2
import torch
import numpy as np
import pytesseract
from PIL import Image
import json
import portalocker
import os
import time
import sharedStatus
from google.cloud import vision
import base64
from googleapiclient import discovery
import subprocess
import signal
import sys
from threading import Thread
import requests
import base64
import io


def capture_frames(output_dir, capture_interval=2):
    if not os.path.isdir(output_dir):
        os.makedirs(output_dir)

    while True:
        ffmpeg_command = f'ffmpeg -i rtmp://localhost/live -vf fps=1/{capture_interval} -q:v 2 -vframes 1 {output_dir}/temp_frame.png'

        process = subprocess.run(ffmpeg_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, creationflags=subprocess.CREATE_NEW_PROCESS_GROUP)
        print(f"Captured a frame to {output_dir}")

        # Wait for the interval before capturing the next frame
        time.sleep(capture_interval)
# Include the FFmpeg capture in the process_images function

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
print(f'Device: {device}')
# Function to load the model
def load_yolo_model(model_path):
    model = torch.hub.load('ultralytics/yolov5', 'custom', path=model_path)
    return model

def run_inference(model, image_path):
    img = cv2.imread(image_path)
    results = model(img)
    return results

# Function to check if the detected scene is scene_gameplay
def check_if_scene_gameplay(scene_classes):
    # Assuming scene_gameplay has the class_id 0, change this based on your model
    scene_gameplay_class_id = 0
    is_scene_gameplay = np.any(scene_classes == scene_gameplay_class_id)
    return is_scene_gameplay

# Function to extract bounding boxes and classes
def extract_bbox_and_classes(results):
    detections = results.pred[0]
    data = detections.detach().cpu().numpy()
    bbox_and_classes = []
    for entry in data:
        x1, y1, x2, y2, conf, class_id = entry
        bbox_and_classes.append({
            'bbox': (x1, y1, x2, y2),
            'class_id': int(class_id)
        })
    return bbox_and_classes

MY_API_KEY = 'AIzaSyDvcyEZm5Qewf2WgN8dhhooTDQRmYJqwOk'

"""def extract_text_from_image(img, bbox, mode='tesseract', language_code='jpn',  tessdata_dir='C:/Program Files/Tesseract-OCR/tessdata'):
    x1, y1, x2, y2 = bbox
    x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
    cropped_image = img[y1:y2, x1:x2]
    pil_img = Image.fromarray(cropped_image)

    if mode == 'google':
        # Encode image bytes to base64
        img_str = pil_img.tobytes()
        img_base64 = base64.b64encode(img_str).decode('utf-8')

        # Set up the client and request
        service = discovery.build('vision', 'v1', developerKey=MY_API_KEY, static_discovery=False)
        request = {
            'requests': [
                {
                    'image': {
                        'content': img_base64
                    },
                    'features': [
                        {
                            'type': 'DOCUMENT_TEXT_DETECTION'
                        }
                    ],
                    'imageContext': {
                        'languageHints': ['ja']
                    }
                }
            ]
        }

        # Send request and get response
        response = service.images().annotate(body=request).execute()
        if 'fullTextAnnotation' in response['responses'][0]:
            extracted_text = response['responses'][0]['fullTextAnnotation']['text']
        else:
            print(f"No text detected or an error occurred for image: {img}")
            extracted_text = ""

    elif mode == 'tesseract':
        extracted_text = pytesseract.image_to_string(pil_img, config=f'-c preserve_interword_spaces=1 -l {language_code} --tessdata-dir "{tessdata_dir}"')

    else:
        raise ValueError('Invalid mode. Choose either "google" or "tesseract".')

    return extracted_text.strip()"""
def extract_text_from_image(img, bbox, mode='google', language_code='jpn', tessdata_dir='C:/Program Files/Tesseract-OCR/tessdata'):
    x1, y1, x2, y2 = bbox
    x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
    cropped_image = img[y1:y2, x1:x2]
    pil_img = Image.fromarray(cropped_image)
    cropped_images_dir = ".\\temp\\cropped_images"
    os.makedirs(cropped_images_dir, exist_ok=True)
    cropped_image_filename = f"{time.strftime('%Y%m%d-%H%M%S')}-cropped_image.png"
    cropped_image_path = os.path.join(cropped_images_dir, cropped_image_filename)
    pil_img.save(cropped_image_path)
    print(f"Cropped image saved at {cropped_image_path}")
    if mode == 'google':
        # Encode image bytes to base64
        img_byte_arr = io.BytesIO()
        pil_img.save(img_byte_arr, format='PNG')
        img_base64 = base64.b64encode(img_byte_arr.getvalue()).decode('utf-8')

        # Set up the request
        url = 'https://vision.googleapis.com/v1/images:annotate'
        api_key = MY_API_KEY  # Replace with your API Key
        headers = {'Content-Type': 'application/json'}
        data = {
            'requests': [
                {
                    'image': {
                        'content': img_base64
                    },
                    'features': [
                        {
                            'type': 'DOCUMENT_TEXT_DETECTION'
                        }
                    ],
                    'imageContext': {
                        'languageHints': ['ja']
                    }
                }
            ]
        }

        # Send request and get response
        response = requests.post(url, headers=headers, json=data, params={'key': api_key})
        response.raise_for_status()
        response_data = response.json()

        if 'fullTextAnnotation' in response_data['responses'][0]:
            extracted_text = response_data['responses'][0]['fullTextAnnotation']['text']
        else:
            print(f"No text detected or an error occurred for image: {img}")
            extracted_text = ""

    elif mode == 'tesseract':
        extracted_text = pytesseract.image_to_string(pil_img, config=f'-c preserve_interword_spaces=1 -l {language_code} --tessdata-dir "{tessdata_dir}"')

    else:
        raise ValueError('Invalid mode. Choose either "google" or "tesseract".')

    return extracted_text.strip()

def process_image(frame_path, btl_scene_model, btl_gameplay_model):
    scene_results = run_inference(btl_scene_model, frame_path)
    scene_classes = scene_results.pred[0][:, -1].cpu().numpy()
    is_scene_gameplay = check_if_scene_gameplay(scene_classes)
    print(is_scene_gameplay)
    bbox_and_text= {}   
    if is_scene_gameplay:
        gameplay_results = run_inference(btl_gameplay_model, frame_path)
        bbox_and_classes = extract_bbox_and_classes(gameplay_results)
        img = cv2.imread(frame_path)
        for result in bbox_and_classes:
            bbox = result['bbox']
            bbox_standard = tuple(map(int, bbox)) 
            class_id = result['class_id']

            # Extract text using OCR
            extracted_text = extract_text_from_image(img, bbox)
            print(f"Class: {class_id}, BBox: {bbox}, Extracted Text: {extracted_text}")
            bbox_and_text[class_id] = {'bbox': bbox_standard, 'text': extracted_text}
     
        return img, bbox_and_text
    else:
        return None, None
print("Current working directory:", os.getcwd())
# Load your pre-trained models
btl_scene_model = load_yolo_model('ocr_python/btm/BTL_Scene.pt')
btl_gameplay_model = load_yolo_model('ocr_python/btm/BTL_Gameplay_old.pt')

def process_images(btl_scene_model, btl_gameplay_model):
    capture_output_dir = ".\\temp\\img"
    capture_interval = 1
    # Start the FFmpeg capture in a separate thread
    capture_thread = Thread(target=capture_frames, args=(capture_output_dir, capture_interval))
    capture_thread.start()

    # Change the frame filename to 'current_frame.png'
    frame_file = 'current_frame.png'

    while True:
        frame_path = os.path.join(capture_output_dir, frame_file)
        temp_frame_path = os.path.join(capture_output_dir, 'temp_frame.png')

        if os.path.exists(temp_frame_path):
            os.rename(temp_frame_path, frame_path)
            print(f"Processing {frame_path}...")
            img, bbox_and_text = process_image(frame_path, btl_scene_model, btl_gameplay_model)
            if img is not None and bbox_and_text:
                # Save each json file in 'json' directory using the timestamp as filename
                frame_number = len(os.listdir('./temp/json')) + 1
                json_path = os.path.join('./temp/json', f"frame_{frame_number}.json")
                with portalocker.Lock(json_path, 'w') as file:
                    json.dump(bbox_and_text, file)
                    file.flush()
                    os.fsync(file.fileno())
                    if not sharedStatus.sharedStatus.status['first_update_done']:
                        sharedStatus.sharedStatus.set_ready(True)
                        print("The first successful inference happened")
                for class_id, data in bbox_and_text.items():
                    bbox = data['bbox']
                    text = data['text']

            # Delete the processed frame
            os.remove(frame_path)

        # Wait before checking the directory again to reduce CPU usage
        time.sleep(1)

if __name__ == '__main__':
    btl_scene_model = load_yolo_model('ocr_python/btm/BTL_Scene.pt')
    btl_gameplay_model = load_yolo_model('ocr_python/btm/BTL_Gameplay_old.pt')
    process_images(btl_scene_model, btl_gameplay_model)
