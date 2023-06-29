
import sys
import json
import os
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QColor, QPalette, QFont, QPainter
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow
from json import JSONDecodeError
import sharedStatus
import time

class Overlay(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)

        # Set the desired frame rate (e.g., 1 FPS => 1000ms interval)
        self.update_interval = 1000  # for 1 FPS

        # Set the font size (change the number to your preferred size)
        self.font_size = 12

        # Create QLabel widgets for each text item
        self.labels = {}

        self.frame_counter = 1
        # Set the overlay geometry to cover the full screen (1920*1080)
        self.setGeometry(0, 0, 1920, 1080)
        self.test_label = QLabel(self)
        self.test_label.setFont(QFont("Noto Sans CJK JP", self.font_size))
        self.test_label.setAutoFillBackground(True)
        palette = self.test_label.palette()
        palette.setColor(QPalette.Background, QColor(0, 0, 0, 128))  # ARGB
        palette.setColor(QPalette.WindowText, Qt.white)
        self.test_label.setPalette(palette)
        self.test_label.move(50, 50)
        self.test_label.setText(f"Update #{self.frame_counter}")

        # Start the QTimer with the specified interval
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_overlay)
        self.timer.start(self.update_interval)

        self.frame_counter = 1

    def update_overlay(self):
        # Get the list of all JSON files and sort them
        json_files = sorted([f for f in os.listdir('./temp/json') if f.endswith('.json')])

        if not json_files:
            print("No JSON files found, waiting for output from ocr.py.")
            return

        # Find the matching JSON file for the current frame number
        json_filename = None
        for json_file in json_files:
            frame_number = int(json_file.split('_')[1].split('.')[0])

            if frame_number >= self.frame_counter:
                json_filename = os.path.join('./temp/json', json_file)
                self.frame_counter = frame_number
                break

        # If no matching JSON file is found
        if json_filename is None:
            print(f"No JSON file found for frame {self.frame_counter}, waiting for output.")
            return

        # Process the found JSON file
        try:
            with open(json_filename, 'r', encoding='utf-8') as file:
                data = json.load(file)
        except JSONDecodeError:
            print(f"Could not decode JSON from file: {json_filename}")
            return

        print(f'Updating overlay for: {json_filename}')

        # If the data is not empty, update the labels
        if data:
            # Create/update QLabel for each data item
            for key, item in data.items():
                if key not in self.labels:
                    # create new label
                    label = QLabel(self)
                    label.show()
                    label.raise_()
                    # Set the Japanese font (e.g., "NotoSans CJK JP")
                    font = QFont("Noto Sans CJK JP", self.font_size)
                    font.setStyleStrategy(QFont.PreferAntialias)
                    label.setFont(font)

                    # Set the QLabel positioning
                    x, y, _, _ = item['bbox']
                    label.move(x, y)
                    print(f"Positioning label at: {x}, {y}")

                    # Set the background color and opacity (semi-transparent black)
                    label.setAutoFillBackground(True)
                    palette = label.palette()
                    palette.setColor(QPalette.Background, QColor(0, 0, 0, 128))  # ARGB

                    # Set the text color to white
                    palette.setColor(QPalette.WindowText, Qt.white)
                    label.setPalette(palette)

                    self.labels[key] = label
                    print(f'Created new label: {key}')
                else:
                    label = self.labels[key]
                    print(f'Updated existing label: {key}')

                # Set the text
                label.setText(item['text'])

                # Force the overlay to update and adjust its size based on content
                label.adjustSize()

        self.test_label.setText(f"Update #{self.frame_counter}")
        self.test_label.adjustSize()

        self.frame_counter += 1

if __name__ == "__main__":
    app = QApplication(sys.argv)
    overlay = Overlay()
    overlay.show()

    sys.exit(app.exec_())