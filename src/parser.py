import re
from bs4 import BeautifulSoup

class EmailParser:
    @staticmethod
    def clean_filename(subject):
        """Sanitize string for file system safety."""
        return re.sub(r'[\\/*?:"<>|]', "", subject).strip().replace(" ", "_")

    @staticmethod
    def html_to_markdown(html_content):
        """Convert raw HTML to readable text/markdown."""
        soup = BeautifulSoup(html_content, "html.parser")
        
        # Simple extraction - you can add more logic here later
        # e.g., finding all <a> tags and formatting them as [Link](url)
        text = soup.get_text(separator="\n\n")
        
        # Remove excessive whitespace
        return re.sub(r'\n\s*\n', '\n\n', text).strip()

    @staticmethod
    def parse_body(msg):
        """Extract content from email object."""
        body = ""
        if msg.is_multipart():
            for part in msg.walk():
                content_type = part.get_content_type()
                if content_type == "text/plain":
                    body += part.get_payload(decode=True).decode(errors="ignore")
                elif content_type == "text/html":
                    html_content = part.get_payload(decode=True).decode(errors="ignore")
                    body += EmailParser.html_to_markdown(html_content)
        else:
            payload = msg.get_payload(decode=True).decode(errors="ignore")
            if msg.get_content_type() == "text/html":
                body = EmailParser.html_to_markdown(payload)
            else:
                body = payload
        return body