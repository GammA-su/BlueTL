import os
import shutil
import subprocess
import sys
import signal
import time
import keyboard

def run_script(script_name):
    print(f"Running {script_name}...")
    process = subprocess.Popen([sys.executable, script_name], creationflags=subprocess.CREATE_NEW_PROCESS_GROUP)
    print(f"{script_name} is now running.")
    return process

def main():
    try:
        # Replace 'ocr.py', 'overlay.py' with the actual paths if they are not in the same directory
        scripts = ['ocr_python/ocr.py', 'ocr_python/overlay.py']
        processes = []

        for script in scripts:
            process = run_script(script)
            processes.append(process)

        for process in processes:
            process.communicate()

    except KeyboardInterrupt:
        print("\nCtrl+C detected. Terminating all processes...")

        for process in processes:
            process.send_signal(signal.SIGTERM)
            process.wait()
            print(f"Terminated process with pid {process.pid}")

        print("All processes have been terminated.")

if __name__ == "__main__":
    main()