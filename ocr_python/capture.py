import time
import cv2
import os
import numpy as np
from PIL import Image
import pygetwindow as gw
import win32gui
import win32ui
from ctypes import windll

def capture_window(hwnd):
    left, top, right, bottom = win32gui.GetWindowRect(hwnd)
    width = right - left
    height = bottom - top

    hWndDC = win32gui.GetWindowDC(hwnd)
    mfcDC = win32ui.CreateDCFromHandle(hWndDC)
    saveDC = mfcDC.CreateCompatibleDC()

    saveBitMap = win32ui.CreateBitmap()
    saveBitMap.CreateCompatibleBitmap(mfcDC, width, height)

    saveDC.SelectObject(saveBitMap)

    windll.gdi32.BitBlt(saveDC.GetSafeHdc(), 0, 0, width, height, mfcDC.GetSafeHdc(), 0, 0, 13369376)

    bmpinfo = saveBitMap.GetInfo()
    bmpstr = saveBitMap.GetBitmapBits(True)

    img = Image.frombuffer('RGB', (bmpinfo['bmWidth'], bmpinfo['bmHeight']), bmpstr, 'raw', 'BGRX', 0, 1)

    win32gui.DeleteObject(saveBitMap.GetHandle())
    saveDC.DeleteDC()
    mfcDC.DeleteDC()
    win32gui.ReleaseDC(hwnd, hWndDC)

    return np.array(img)

# Function to delete the N oldest images from the directory
def delete_oldest_images(directory, n):
    sorted_images = sorted(os.listdir(directory), key=lambda x: os.path.getctime(os.path.join(directory, x)))
    for i in range(min(n, len(sorted_images))):
        try:
            os.remove(os.path.join(directory, sorted_images[i]))
        except Exception as e:
            print(f"Error deleting image: {e}")

os.makedirs("temp/img", exist_ok=True)

# Replace 'your_application_exe_name.exe' with your game/application's executable name
window_name = 'BLUE PROTOCOL'
hwnd = gw.getWindowsWithTitle(window_name)[0]._hWnd

fps = 1
frame_counter = 0
while True:
    start_time = time.time()

    frame = capture_window(hwnd)
    frame_path = f"temp/img/frame_{frame_counter:06d}.jpg"
    cv2.imwrite(frame_path, cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))
    frame_counter += 1

    # Process the frame here, for example, call process_image() with the captured frame

    if frame_counter % 100 == 0:
        delete_oldest_images("temp/img", 50)

    # Wait for the next frame
    time.sleep(max(1./fps - (time.time() - start_time), 0))