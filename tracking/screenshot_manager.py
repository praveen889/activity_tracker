import time
import threading
import pyautogui
import os
from PIL import ImageFilter

class ScreenshotManager:
    def __init__(self, interval=300, blur=False, output_dir="static/screenshots"):
        self.interval = interval
        self.blur = blur
        self.output_dir = output_dir
        self.active = False
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    def capture_screenshot(self):
        screenshot = pyautogui.screenshot()
        if self.blur:
            screenshot = screenshot.filter(ImageFilter.GaussianBlur(15))
        file_path = os.path.join(self.output_dir, f'screenshot_{int(time.time())}.png')
        screenshot.save(file_path)
        print(f"Screenshot saved: {file_path}")

    def start_capturing(self):
        self.active = True
        print("Starting screenshot capturing...")
        while self.active:
            self.capture_screenshot()
            time.sleep(self.interval)

    def stop_capturing(self):
        if self.active:
            print("Stopping screenshot capturing...")
            self.active = False 
            print("Screenshot capturing stopped.")
        else:
            print("Screenshot capturing was not active.")
