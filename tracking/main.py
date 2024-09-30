import threading
from .activity_tracker import ActivityTracker
from .screenshot_manager import ScreenshotManager
from .config_manager import ConfigManager
from .timezone_manager import TimeZoneManager
from .s3_uploader import S3Uploader
import time


class EmployeeAgent:
    def __init__(self, username):
        self.username = username
        self.activity_tracker = ActivityTracker()
        self.screenshot_manager = ScreenshotManager()

    def start(self):
        print("Starting employee agent...")
        self.activity_tracker.start_tracking()
        threading.Thread(target=self.screenshot_manager.start_capturing).start()

    def stop(self):
        print(f"Stopping tracking for user: {self.username}")
        self.activity_tracker.stop_tracking()  # Stop the activity tracker
        self.screenshot_manager.stop_capturing()  # Stop the screenshot manager


    def monitor_timezone_changes(self):
        while True:
            self.timezone_manager.check_timezone_change()
            time.sleep(60)

if __name__ == "__main__":
    agent = EmployeeAgent()
    agent.start()
