import imaplib
import email
import ssl
from config import Config

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

            print(f"Connected to {email_config['server']}")
            return True

        except Exception as e:
            print(f"Connection failed: {e}")
            return False

    def disconnect(self):
        if self.mail:
            self.mail.close()
            self.mail.logout()
            print("Disconnected from email server")

    def get_folders(self):
        if not self.mail:
            return []

        status, folders = self.mail.list()
        if status == 'OK':
            return [folder.decode().split('"')[-2] for folder in folders]
        return []