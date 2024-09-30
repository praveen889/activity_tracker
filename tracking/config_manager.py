import json
import os

class ConfigManager:
    def __init__(self, config_file="config.json"):
        self.config_file = config_file
        self.config = self.load_config()

    def load_config(self):
        if os.path.exists(self.config_file):
            with open(self.config_file, 'r') as file:
                return json.load(file)
        else:
            return {"screenshot_interval": 300, "blur_screenshots": False}

    def save_config(self, new_config):
        with open(self.config_file, 'w') as file:
            json.dump(new_config, file)
        self.config = new_config

    def update_config(self, key, value):
        self.config[key] = value
        self.save_config(self.config)
