import time
import threading
import pyautogui
import os
from PIL import ImageFilter

class ScreenshotManager:
    def __init__(self, user_id, log_callback, upload_callback=None, interval=60):
        self.user_id = user_id
        self.log_callback = log_callback
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
        
        if self.log_callback:
            self.log_callback(screenshot_path=file_path)
            
        return file_path 

    def start_capturing(self):
        if not self.active:
            self.active = True
            print("Starting screenshot capturing...")
            self.capture_thread = threading.Thread(target=self.capture_loop)
            self.capture_thread.start()

    def capture_loop(self):
        while self.active:
            print("Capturing screenshot...") 
            self.capture_screenshot()
            time.sleep(self.interval)
        print("Capture loop has exited.") 

    def stop_capturing(self):
        print("Attempting to stop screenshot capturing...")
        if self.active:
            self.active = False 
            if self.capture_thread is not None:
                self.capture_thread.join() 
            print("Screenshot capturing stopped.")
        else:
            print("Screenshot capturing was not active.")
