import json
import os

class Config:
    def __init__(self, config_file="config.json"):
        self.config_file = config_file
        self.config = self.load_config()

    def load_config(self):
        if os.path.exists(self.config_file):
            with open(self.config_file, 'r') as f:
                return json.load(f)
        return self.default_config()

    def default_config(self):
        return {
            "email": {
                "server": "",
                "username": "",
                "password": "",
                "port": 993
            },
            "rules": []
        }

    def save_config(self):
        with open(self.config_file, 'w') as f:
            json.dump(self.config, f, indent=2)