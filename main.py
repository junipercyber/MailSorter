#!/usr/bin/env python3

import os
from email_client import EmailClient
from config import Config

def main():
    print("MailSorter - Email Classification Tool")

    if not os.path.exists("config.json"):
        print("Config file not found. Please create config.json based on config.json.example")
        return

    client = EmailClient()

    if client.connect():
        folders = client.get_folders()
        print(f"Available folders: {folders}")
        client.disconnect()
    else:
        print("Failed to connect to email server")

if __name__ == "__main__":
    main()