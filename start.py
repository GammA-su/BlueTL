import os
import os.path
import shutil
import subprocess
import sys
import signal
import keyboard
import platform
import pathlib
from time import sleep
import glob
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import textwrap
import time
import argparse
from google.cloud import storage
from google.api_core.exceptions import Forbidden

CHECK_MARK = "\u2713"
time_preset = 2

def parse_arguments():
    parser = argparse.ArgumentParser(description='BlueTL - Accurate OCR accelerated with Machine Learning')
    parser.add_argument('-v', '--verbose', action='store_true', help='Enable verbose mode')
    # Add new arguments
    parser.add_argument('-c', '--capture', action='store_true', help='Enable frame capture mode')
    parser.add_argument('-i', '--interval', type=int, default=15, help='Frame capture interval in seconds')
    parser.add_argument('-b', '--bucket', type=str, default="datacollection70", help='Google Cloud Storage bucket end directory MUST CHANGED EACH SEESION!')
    args = parser.parse_args()
    return args

def print_welcome_message(verbose):
    os.system("cls" if os.name == "nt" else "clear")
    if verbose : 
        print("Verbose mode activated")
    print("\033[1;34;40mWelcome to BlueTL\033[0m")
    print("\033[1;36;40m------> Accurate OCR accelerated with Machine Learning\033[0m")
    print("\033[1;37;40m")
    print("+-" * 38 + "+")
    print(f"{' ' * 15}\033[1;33;40mPlease ensure FFmpeg and Nginx are installed!\033[0m")
    print("+-" * 38 + "+")
    print("\033[0m")
    

def check_if_installed(verbose,executable, is_nginx=False):
    if verbose : 
        print("--- Check if installed function called!")
    try:
        if is_nginx:
            nginx_check_path = ".\\rtmp_server\\nginx_check.bat"
            if os.path.exists(nginx_check_path):
                if verbose : 
                    print("--- def cih-- Path exist !")
                    
                result = subprocess.run(nginx_check_path, shell=True, stdout=subprocess.PIPE)
                if verbose : 
                    print("--- def cih-- subprocess result assigned !")
                if result.returncode == 2:
                    if verbose : 
                        print("--- def cih-- Return 2 !")
                    return False
                elif result.returncode == 1:
                    if verbose :
                        print("--- def cih-- Return 1 !")
                    return True
            else:
                if verbose :
                    print("--- def cih-- else !")
                print("Could not find nginx_check.bat file. Please ensure the file exists.")
                return False
        
        subprocess.call([executable, "--version"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return True
    except FileNotFoundError:
        return False
def install_ffmpeg(verbose):
    if verbose :
        print("--- def iff-- Function Called !")
    print("Installing FFmpeg")
    os.system("install_ffmpeg.bat")  # Replace with your actual FFmpeg installation script

def install_nginx_and_launch(verbose):
    if verbose :
        print('---def inal--- Function Called!')
    result = subprocess.call(".\\rtmp_server\\nginx_install.bat", shell=True)
    if verbose :
            print('---def inal--- Result :'+result)
    if result != 1:
        if verbose :
            print('---def inal--- Return not 1 :')
        print("\033[1;31;40mAn error occurred during Nginx installation and launch.\033[0m")
        sys.exit(1)
    else:
        if verbose :
            print('---def inal--- Return  1/Else :')
        print("\033[1;32;40mNginx is installed and running.\033[0m")

def move_obs_ini_file(verbose):
    obs_default_path = os.path.join(os.getenv("APPDATA"), "obs-studio")
    if verbose :
        print('---def moif--- Function Called!')
    """if platform.system() == "Windows":
        obs_default_path = os.path.expanduser(r"~\\AppData\\Roaming\\obs-studio\\basic\\profiles")"""
    if platform.system() == "MacOS":
        print("\033[1;32;40m MacOS is not supported at the moment! Please excuse us for the inconvenience \033[0m")
    elif platform.system() == "Linux":
        print("\033[1;32;40m Linux is not supported at the moment! Please excuse us for the inconvenience \033[0m")
    src_folder = "config/bluetl"
    dest_folder = os.path.join(obs_default_path, "basic", "profiles", "bluetl")
    if os.path.exists(dest_folder):
        shutil.rmtree(dest_folder)
    shutil.copytree(src_folder, dest_folder)
    print("\033[1;32;40mOBS configuration 'bluetl' folder has been copied successfully.\033[0m")

def check_is_nginx_running(verbose):
    if verbose :
        print('---def cinr--- Function Called!')
    nginx_check_path = ".\\rtmp_server\\nginx_check.bat"
    if os.path.exists(nginx_check_path):
        if verbose :
            print('---def moif--- path Exist!')
        result = subprocess.run(nginx_check_path, shell=True, stdout=subprocess.PIPE)
        if result.returncode == 1:
            return True
        if result.returncode == 0:
            return False
    else:
        if verbose :
            print('---def moif--- Path doesnt exist Else!')
        print("Could not find nginx_check.bat file. Please ensure the file exists.")
        return False
# ... (rest of the functions are unchanged) ... MAIN 

        
def run_script(verbose,script_name):
    if verbose :
        print('---def rs--- Function Called!')
    print(f"Running {script_name}...")
    process = subprocess.Popen([sys.executable, script_name], creationflags=subprocess.CREATE_NEW_PROCESS_GROUP)
    print(f"{script_name} is now running.")
    return process

def clear_directory(verbose,directory):
    if verbose :
        print('---def cd--- Function Called!')
    for item in os.listdir(directory):
        item_path = os.path.join(directory, item)
        if os.path.isfile(item_path):
            os.unlink(item_path)
        elif os.path.isdir(item_path):
            shutil.rmtree(item_path)
def waitForKeyPress(verbose,key):  # Add this function to wait for key press
    if verbose :
        print('---def waitkey--- Function Called!')
    while True:
        if keyboard.is_pressed(key):
            if verbose :
                print('---def waitkey--- Key Pressed!!')
            break

def ask_permission_and_install(verbose,install_function, software_name):
    if verbose :
        print('---def apan--- Function Called!')
    print(f"\033[1;31;40m{software_name} not installed and needed for OCR.\033[0m")
    response = input(f"Do you want to install {software_name}? (y/n): ").lower()
    if response == 'y' or response == 'yes':
        install_function(verbose)
    else:
        print(f"\033[1;31;40m{software_name} installation aborted.\033[0m")
        sys.exit(1)
        # TEST
        #
        #

def display_message(message):
    border = "-" * len(message)
    print("\033[1;36;40m")
    print(" " + border)
    print(" " + message)
    print(" " + border)
    print("\033[0m")

def perform_verification(verbose):
    display_message("Configuration Completed")

    print("Please follow these steps to setup OBS:")
    instructions = """
    1. Open OBS Studio.
    2. Make sure Blue Protocol is selected as the window/source.
    3. Start the recording (not streaming).

    You will need to review an image and say yes if it is Blue Protocol. Please LOOK FOR THE WINDOW IN THE TASKBAR
    """
    print(textwrap.dedent(instructions))
    display_message("FOR THE FOLLOWING STEPS ONLY (unrelated to the current confirmation)! LOOK FOR AN OTHER WINDOW SHOWING THE IMAGE IN THE TASKBAR!!!")
    while True:
        verification = input("Have you completed the above steps? (y/n): ").lower()
        if verification in ["yes", "y"]:
            return True
        elif verification in ["no", "n"]:
            return False
        elif verification in ["nanahira", "n7"]:
            if verbose :
                print('---def pv--- Straight to Buisness!!')
            start_launcher_ocr()



def start_test():
    display_message("Test Beginning")
    cmd_ffmpeg = "ffmpeg -i rtmp://localhost/live -vf fps=1/1 -vframes 3 ./temp/frames_%04d.png  >nul 2>&1"
    process = subprocess.run(cmd_ffmpeg, shell=True)
    temp_files = glob.glob("./temp/frames_*.png")
    if len(temp_files) >= 1:
        img = mpimg.imread(temp_files[0])  # Display the first frame
        imgplot = plt.imshow(img)
        plt.show()
        wait_duration = time_preset  # seconds
        plt.pause(wait_duration)  # Wait for the specified duration
        plt.close()  # Close the window

        while True:
            validation = input("Is the displayed image from Blue Protocol? (y/n): ").lower()
            if validation in ["yes", "y"]:
                display_message("Test Passed! \u2713")
                return True
            elif validation in ["no", "n"]:
                display_message("Test Failed! \u2718")
                return False
    else:
        print("Error: Unable to obtain any frames for testing.")
        sys.exit(1)

def check_required_files():
    required_files = [
        ".\\ocr_python\\overlay.py",
        ".\\ocr_python\\ocr.py",
        ".\\cpp_launcher\\BlueTL_launcher.exe",
    ]
    all_files_exist = True
    for file_path in required_files:
        if not os.path.exists(file_path):
            print(f"Error: Required file '{file_path}' is missing.")
            all_files_exist = False
    return all_files_exist

def start_launcher_ocr():
    print("\033[1;37;40mBlueTL_launcher.exe will open now.\033[0m")
    subprocess.Popen("cmd.exe /c start .\\cpp_launcher\\BlueTL_launcher.exe", shell=True)
    print("\033[1;37;40mPlease press the Blue Protocol button and choose the path of blueprotocol.exe.\033[0m")
    print("\033[1;36;40mNote: Do NOT choose the shipping... .exe file.\033[0m")
    input("\033[1;33;40mPress Enter to continue after choosing the path of blueprotocol.exe...\033[0m")
    
    print("\033[1;37;40mocr.py will start in 10 seconds.\033[0m")
    time.sleep(3)
    
    # Start ocr.py
    try:
        verbose = parse_arguments()
        ocr_process = run_script(verbose,".\\ocr_python\\main.py")
        print(f"main.py has started.")
    except FileNotFoundError:
        print("\033[1;31;40mError: Could not find main.py.\033[0m")
        sys.exit(1)

def capture_frames(verbose, interval, save_path):
    print(f"\n[INFO] Capturing frames every {interval} seconds...\n")
    args = parse_arguments()
    counter = 0
    
    while True:
        current_frame_file = f"{save_path}/frames_{counter:04d}.png"
        cmd_ffmpeg = f"ffmpeg -i rtmp://localhost/live -vf fps=1/{interval} -vframes 1 {current_frame_file} >nul 2>&1"
        subprocess.run(cmd_ffmpeg, shell=True)
        upload_to_gcloud(verbose, current_frame_file, args.bucket)
        
        counter += 1
        time.sleep(interval)
def upload_to_gcloud(verbose, file_path, bucket_end):
    bucket_name = 'blue.2kken.com'
    print(f"\n[INFO] Uploading frames to Google Cloud bucket: {bucket_name}...\n")
    
    client = storage.Client()
    bucket = client.bucket(bucket_name)

    try :
        blob = bucket.blob(f"{bucket_end}/{os.path.basename(file_path)}")
        blob.upload_from_filename(file_path)
        print(f"Uploaded {file_path} to {bucket_name}.")
    except Forbidden as e :
        print("You must change directory! Use -b datacollection07 for example.")
        return

def dependanceCheck(verbose):
    clear_directory(verbose,".\\temp\\")
    os.makedirs('.\\temp\\json\\')
    print_welcome_message(verbose)

    print("\033[1;37;40mChecking for FFmpeg installation...\033[0m", end="")
    ffmpeg_installed = check_if_installed(verbose,"ffmpeg",is_nginx=False)
    if ffmpeg_installed:
        print(f"\033[1;32;40m {CHECK_MARK}\033[0m")
    else:
        ask_permission_and_install(install_ffmpeg, "FFmpeg",verbose)
        print("\033[1;37;40mFFmpeg installed successfully.\033[1;32;40m {}\033[0m".format(CHECK_MARK))

    print("\033[1;37;40mChecking for Nginx installation...\033[0m", end="")
    nginx_installed = check_if_installed(verbose, "nginx", is_nginx=True)
    if nginx_installed:
        print(f"\033[1;32;40m {CHECK_MARK}\033[0m")
    else:
        ask_permission_and_install(verbose,install_nginx_and_launch, "Nginx")
        print("\033[1;37;40mNginx installed successfully.\033[1;32;40m {}\033[0m".format(CHECK_MARK))

    print("\033[1;37;40mChecking if Nginx is running...\033[0m", end="")
    if check_is_nginx_running(verbose):
        print(f"\033[1;32;40m {CHECK_MARK}\033[0m")
    else:
        print("\033[1;37;40mStarting Nginx...\033[0m", end="")
        if check_is_nginx_running(verbose):
            print(f"\033[1;32;40m {CHECK_MARK}\033[0m")
        else:
            print("\033[1;31;40mError: Nginx failed to start.\033[0m")
            sys.exit(1)

def capture_mode(verbose,args):
        project_root = os.path.dirname(os.path.realpath(__file__))
        service_account_key_path = os.path.join(project_root, "config", "google_auth_datacollection.json")
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = service_account_key_path
        save_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'temp/data_collection')
        os.makedirs(save_path, exist_ok=True)
        display_message("Data will be captured to supply datasets, Thanks for your help!")
        
        # Capture frames
        capture_frames(verbose, args.interval, save_path)

        

def main():
    args = parse_arguments()
    verbose = args.verbose
    dependanceCheck(verbose)

    move_obs_ini_file(verbose)

    if not perform_verification(verbose):
        clear_directory(".\\temp\\")
        print("Verification failed. Exiting the program.")
        sys.exit(1)

    if start_test():
        if check_required_files():
            print("Test Passed! Now you can proceed with the OCR.")
            # Your next steps...
        else:
            print("Test failed. Please fix the issue and rerun the program.")
            sys.exit(1)
    if args.capture:
        capture_mode(verbose,args)
    else:
        print("Test failed. Please fix the issue and rerun the program.")
        sys.exit(1)

    

if __name__ == "__main__":
    main()