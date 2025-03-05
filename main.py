#!/usr/bin/env python3

import os
import argparse
from email_client import EmailClient
from config import Config
from sorter import MailSorter

def list_folders(client):
    folders = client.get_folders()
    print("Available folders:")
    for folder in folders:
        print(f"  - {folder}")

def test_connection(client):
    if client.connect():
        print("Connection successful!")
        list_folders(client)
        client.disconnect()
    else:
        print("Connection failed!")

def sort_emails(client, limit=10, dry_run=True):
    if not client.connect():
        print("Failed to connect to email server")
        return

    config = Config()
    sorter = MailSorter(config.config.get('rules', []))

    emails = client.get_emails(limit=limit)
    print(f"Processing {len(emails)} emails...")

    moved_count = 0
    required_folders = set()

    for email_id, email_message in emails:
        folder = sorter.classify_email(email_message)
        subject = email_message.get('Subject', 'No Subject')[:50]

        if folder != 'INBOX':
            required_folders.add(folder)

        if dry_run:
            print(f"Would move '{subject}' to folder '{folder}'")
        else:
            print(f"Moving '{subject}' to folder '{folder}'")
            if client.move_email(email_id, folder):
                moved_count += 1

    if not dry_run:
        print(f"Successfully moved {moved_count} emails")

        if required_folders:
            existing_folders = client.get_folders()
            for folder in required_folders:
                if folder not in existing_folders:
                    client.create_folder(folder)

    client.disconnect()

def main():
    parser = argparse.ArgumentParser(description='MailSorter - Email Classification Tool')
    parser.add_argument('--test', action='store_true', help='Test connection')
    parser.add_argument('--sort', action='store_true', help='Sort emails')
    parser.add_argument('--limit', type=int, default=10, help='Number of emails to process')
    parser.add_argument('--no-dry-run', action='store_true', help='Actually move emails')

    args = parser.parse_args()

    if not os.path.exists("config.json"):
        print("Config file not found. Please create config.json based on config.json.example")
        return

    client = EmailClient()

    if args.test:
        test_connection(client)
    elif args.sort:
        sort_emails(client, limit=args.limit, dry_run=not args.no_dry_run)
    else:
        print("MailSorter - Email Classification Tool")
        print("Use --help for available options")

if __name__ == "__main__":
    main()