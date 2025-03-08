#!/usr/bin/env python3

import json
import getpass
from config import Config

def setup_config():
    print("MailSorter Configuration Setup")
    print("=" * 30)

    config_data = {
        "email": {
            "server": input("IMAP Server (e.g., imap.gmail.com): ").strip(),
            "username": input("Email address: ").strip(),
            "password": getpass.getpass("Password: "),
            "port": 993
        },
        "rules": []
    }

    print("\nEmail Rules Setup (press Enter to skip)")
    rule_count = 1

    while True:
        print(f"\nRule #{rule_count}:")
        name = input("Rule name (or press Enter to finish): ").strip()
        if not name:
            break

        folder = input("Target folder: ").strip()
        keywords = input("Keywords (comma-separated): ").strip()
        sender_patterns = input("Sender patterns (comma-separated): ").strip()

        rule = {
            "name": name,
            "folder": folder
        }

        if keywords:
            rule["keywords"] = [k.strip() for k in keywords.split(",")]
        if sender_patterns:
            rule["sender_patterns"] = [p.strip() for p in sender_patterns.split(",")]

        config_data["rules"].append(rule)
        rule_count += 1

    with open("config.json", "w") as f:
        json.dump(config_data, f, indent=2)

    print("\nConfiguration saved to config.json")

    config = Config()
    errors = config.validate_config()
    if errors:
        print("Warning: Configuration has issues:")
        for error in errors:
            print(f"  - {error}")
    else:
        print("Configuration is valid!")

if __name__ == "__main__":
    setup_config()