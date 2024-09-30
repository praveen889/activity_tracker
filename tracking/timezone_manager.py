import time

class TimeZoneManager:
    def __init__(self):
        self.last_timezone = self.get_current_timezone()

    def get_current_timezone(self):
        return time.tzname

    def check_timezone_change(self):
        current_timezone = self.get_current_timezone()
        if current_timezone != self.last_timezone:
            print(f"Timezone changed from {self.last_timezone} to {current_timezone}")
            self.last_timezone = current_timezone
