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

    def validate_config(self):
        errors = []

        email_config = self.config.get('email', {})
        required_fields = ['server', 'username', 'password']

        for field in required_fields:
            if not email_config.get(field):
                errors.append(f"Missing email.{field}")

        port = email_config.get('port', 993)
        if not isinstance(port, int) or port <= 0:
            errors.append("Invalid email.port (must be positive integer)")

        rules = self.config.get('rules', [])
        for i, rule in enumerate(rules):
            if not rule.get('name'):
                errors.append(f"Rule {i}: missing name")
            if not rule.get('folder'):
                errors.append(f"Rule {i}: missing folder")
            if not any(key in rule for key in ['keywords', 'sender_patterns']):
                errors.append(f"Rule {i}: must have keywords or sender_patterns")

        return errors