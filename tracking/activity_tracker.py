import threading
import time
import os
import datetime
from pynput import mouse, keyboard
from PIL import ImageGrab
from utils.s3_utils import upload_db_to_s3

class ActivityTracker:
    def __init__(self, user_id, log_callback):
        self.user_id = user_id
        self.log_callback = log_callback
        self.mouse_movements = []
        self.keyboard_inputs = []

    def start_tracking(self):
        self.is_tracking = True
        self.track_thread = threading.Thread(target=self.track)
        self.track_thread.start()

    def stop_tracking(self):
        self.is_tracking = False
        if self.track_thread.is_alive():
            self.track_thread.join()

    def track(self):
        with mouse.Listener(on_move=self.on_move) as mouse_listener, \
             keyboard.Listener(on_press=self.on_key_press) as key_listener:
            while self.is_tracking:
                time.sleep(20)  # Capture every second
            mouse_listener.stop()
            key_listener.stop()

    def on_move(self, x, y):
        if self.is_tracking:
            try:
                self.log_callback(mouse_activity=f"Mouse moved to ({x}, {y})")
            except NotImplementedError as e:
                print(f"Mouse tracking not supported: {e}")

    def on_key_press(self, key):
        if self.is_tracking:
            try:
                self.log_callback(keyboard_activity=f"Key pressed: {key}")
            except NotImplementedError as e:
                print(f"Key tracking not supported: {e}")
class ScreenshotManager:
    def __init__(self, user_id, log_callback, upload_callback=None):
        self.user_id = user_id
        self.log_callback = log_callback
        self.upload_callback = upload_callback

    def start_capturing(self):
        self.is_capturing = True
        self.capture_thread = threading.Thread(target=self.capture_screenshots)
        self.capture_thread.start()

    def stop_capturing(self):
        self.is_capturing = False
        if self.capture_thread.is_alive():
            self.capture_thread.join()

    def capture_screenshots(self):
        while self.is_capturing:
            screenshot_path = self.take_screenshot()
            self.log_callback(screenshot_path=screenshot_path)
            self.upload_callback(screenshot_path)
            time.sleep(60)  # Capture screenshot every 60 seconds

    def take_screenshot(self):
        screenshot_dir = 'screenshots'
        os.makedirs(screenshot_dir, exist_ok=True)
        timestamp = int(time.time())
        screenshot_path = os.path.join(screenshot_dir, f'screenshot_{timestamp}.png')
        ImageGrab.grab().save(screenshot_path)
        return screenshot_path
