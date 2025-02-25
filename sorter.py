import re
import email
from email.header import decode_header

class MailSorter:
    def __init__(self, rules):
        self.rules = rules

    def classify_email(self, mail_message):
        subject = self._get_header(mail_message, 'Subject')
        sender = self._get_header(mail_message, 'From')
        body = self._get_body(mail_message)

        for rule in self.rules:
            if self._matches_rule(rule, subject, sender, body):
                return rule['folder']

        return 'INBOX'

    def _get_header(self, mail_message, header_name):
        header = mail_message.get(header_name, '')
        if header:
            decoded = decode_header(header)[0]
            if decoded[1]:
                return decoded[0].decode(decoded[1])
            return str(decoded[0])
        return ''

    def _get_body(self, mail_message):
        if mail_message.is_multipart():
            for part in mail_message.walk():
                if part.get_content_type() == "text/plain":
                    try:
                        return part.get_payload(decode=True).decode()
                    except:
                        pass
        else:
            try:
                return mail_message.get_payload(decode=True).decode()
            except:
                pass
        return ''

    def _matches_rule(self, rule, subject, sender, body):
        text_to_check = f"{subject} {body}".lower()

        if 'keywords' in rule:
            for keyword in rule['keywords']:
                if keyword.lower() in text_to_check:
                    return True

        if 'sender_patterns' in rule:
            for pattern in rule['sender_patterns']:
                if pattern.lower() in sender.lower():
                    return True

        return False