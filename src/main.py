import os
from email.header import decode_header
from .config import Config
from .client import EmailClient
from .parser import EmailParser

def save_to_file(filename, content):
    filepath = os.path.join(Config.OUTPUT_DIR, filename)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"[+] Saved: {filepath}")

def main():
    # 1. Setup
    Config.check()
    if not os.path.exists(Config.OUTPUT_DIR):
        os.makedirs(Config.OUTPUT_DIR)

    # 2. Connect
    client = EmailClient()
    client.connect()

    # 3. Process
    email_ids = client.search_emails()
    print(f"Found {len(email_ids)} emails.")

    for e_id in email_ids:
        msg = client.fetch_email(e_id)
        if not msg:
            continue

        # Extract Header Info
        subject, encoding = decode_header(msg["Subject"])[0]
        if isinstance(subject, bytes):
            subject = subject.decode(encoding if encoding else "utf-8")
        
        sender = msg.get("From")
        date = msg.get("Date")

        # Parse Body
        body_text = EmailParser.parse_body(msg)

        # Format Markdown
        markdown_content = f"# {subject}\n\n**Sender:** {sender}\n**Date:** {date}\n\n---\n\n{body_text}"
        
        # Save
        filename = f"{EmailParser.clean_filename(subject)}.md"
        save_to_file(filename, markdown_content)

    # 4. Cleanup
    client.close()

if __name__ == "__main__":
    main()