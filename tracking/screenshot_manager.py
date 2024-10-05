import time
import threading
import pyautogui
import os

class ScreenshotManager:
    def __init__(self, user_id, log_callback, upload_callback=None, interval=60):
        self.user_id = user_id
        self.log_callback = log_callback
        self.upload_callback = upload_callback
        self.interval = interval
        self.active = False
        self.capture_thread = None

    def capture_screenshot(self):
        screenshot = pyautogui.screenshot()
        file_path = os.path.join('static/screenshots', f'screenshot_{int(time.time())}.png')
        screenshot.save(file_path)
        self.log_callback(screenshot_path=file_path) 
        print(f"Screenshot saved: {file_path}")

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
