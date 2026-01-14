import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    EMAIL_USER = os.getenv("EMAIL_USER")
    EMAIL_PASS = os.getenv("EMAIL_PASSWORD")
    IMAP_SERVER = os.getenv("IMAP_SERVER")
    OUTPUT_DIR = "output"
    
    # Example: specific sender
    _target = os.getenv("TARGET_EMAIL", "default@example.com") # Fallback if missing
    SEARCH_CRITERIA = f'(FROM "{_target}")'

    @staticmethod
    def check():
        """Ensure creds are loaded before running."""
        if not Config.EMAIL_USER or not Config.EMAIL_PASS:
            raise ValueError("Missing EMAIL_USER or EMAIL_PASSWORD in .env file")