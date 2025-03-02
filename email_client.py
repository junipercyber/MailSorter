import imaplib
import email
import ssl
import logging
from config import Config

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class EmailClient:
    def __init__(self, config_file="config.json"):
        self.config = Config(config_file)
        self.mail = None

    def connect(self):
        try:
            email_config = self.config.config['email']

            context = ssl.create_default_context()
            self.mail = imaplib.IMAP4_SSL(email_config['server'],
                                        email_config['port'],
                                        ssl_context=context)

            self.mail.login(email_config['username'],
                          email_config['password'])

            logging.info(f"Successfully connected to {email_config['server']}")
            return True

        except Exception as e:
            logging.error(f"Connection failed: {e}")
            return False

    def disconnect(self):
        if self.mail:
            try:
                self.mail.close()
                self.mail.logout()
                logging.info("Disconnected from email server")
            except Exception as e:
                logging.warning(f"Error during disconnect: {e}")

    def get_folders(self):
        if not self.mail:
            return []

        status, folders = self.mail.list()
        if status == 'OK':
            return [folder.decode().split('"')[-2] for folder in folders]
        return []

    def select_folder(self, folder='INBOX'):
        if not self.mail:
            return False

        status, _ = self.mail.select(folder)
        return status == 'OK'

    def get_emails(self, folder='INBOX', limit=10):
        if not self.select_folder(folder):
            return []

        status, messages = self.mail.search(None, 'ALL')
        if status != 'OK':
            return []

        email_ids = messages[0].split()
        emails = []

        for email_id in email_ids[-limit:]:
            status, msg_data = self.mail.fetch(email_id, '(RFC822)')
            if status == 'OK':
                email_message = email.message_from_bytes(msg_data[0][1])
                emails.append((email_id, email_message))

        return emails