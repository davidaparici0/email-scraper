import imaplib
import email
from .config import Config

class EmailClient:
    def __init__(self):
        self.mail = imaplib.IMAP4_SSL(Config.IMAP_SERVER)

    def connect(self):
        try:
            self.mail.login(Config.EMAIL_USER, Config.EMAIL_PASS)
            self.mail.select('"[Gmail]/All Mail"') # Use All Mail for Gmail
            print("Connected to IMAP server (All Mail).")
        except Exception as e:
            print(f"Connection failed: {e}")
            raise

    def search_emails(self, criteria=Config.SEARCH_CRITERIA):
        print(f"Searching for: {criteria}")
        status, messages = self.mail.search(None, criteria)
        return messages[0].split()

    def fetch_email(self, email_id):
        """Fetches a single email by ID."""
        res, msg_data = self.mail.fetch(email_id, "(RFC822)")
        for response_part in msg_data:
            if isinstance(response_part, tuple):
                return email.message_from_bytes(response_part[1])
        return None

    def close(self):
        self.mail.close()
        self.mail.logout()