# 📨 Email to Markdown Scraper

> A Python automation tool that extracts newsletter content from IMAP servers, sanitizes HTML, and converts it into clean Markdown for LLM analysis.

![Python](https://img.shields.io/badge/Python-3.14-blue?style=flat&logo=python)
![Dependency Manager](https://img.shields.io/badge/uv-managed-purple)
![License](https://img.shields.io/badge/License-MIT-green)

## 📖 Overview

I built this tool to solve a personal data problem: I subscribe to high-value newsletters but found it difficult to aggregate and analyze the insights programmatically.

This script creates a secure **ETL (Extract, Transform, Load) pipeline** that:

1. **Connects** securely to an email provider via IMAP.
2. **Filters** for specific senders (e.g., tech newsletters).
3. **Parses** complex HTML email bodies into readable Markdown.
4. **Archives** the data locally for further processing by LLMs (like GPT-4 or Llama 3).

## ✨ Key Features

* **Security First:** Uses environment variables (`.env`) for credentials; no hardcoded secrets.
* **Modular Architecture:** Separation of concerns between connection logic (`client.py`), configuration (`config.py`), and data parsing (`parser.py`).
* **Robust Parsing:** Handles multipart emails and converts HTML soup into structured text.
* **Modern Tooling:** Built with `uv` for lightning-fast dependency management.

## 🛠️ Tech Stack

* **Language:** Python 3.14+
* **Libraries:** `imaplib`, `email`, `BeautifulSoup4`, `python-dotenv`
* **Package Manager:** uv

## 🚀 Getting Started

### Prerequisites

* Python 3.14 or higher
* [uv](https://github.com/astral-sh/uv) installed
* An Email App Password (if using Gmail)

### Installation

1. **Clone the repository**
```bash
   git clone https://github.com/YOUR_USERNAME/email-to-markdown-scraper.git
   cd email-to-markdown-scraper
```

2. **Initialize dependencies**

   uv will automatically create the virtual environment and install locked dependencies.
```bash
   uv sync
```

3. **Configure Secrets**

   Create a `.env` file in the root directory:
```bash
   touch .env
```

   Add your credentials (do not share this file!):
```env
   EMAIL_USER=your_email@gmail.com
   EMAIL_PASSWORD=xxxx-xxxx-xxxx-xxxx  # Use App Password!
   IMAP_SERVER=imap.gmail.com
   TARGET_EMAIL="newsletter@example.com"
```

## Usage

Run the scraper using uv:
```bash
uv run -m src.main
```

The script will fetch emails and generate Markdown files in the `output/` directory:
```
output/
├── 2024-01-14_Weekly_Tech_Digest.md
├── 2024-01-07_Python_News.md
└── ...
```

## 📂 Project Structure
```
src/
├── client.py    # Handles IMAP connection and fetching
├── config.py    # Manages environment variables and settings
├── parser.py    # logic for HTML -> Markdown conversion
└── main.py      # Entry point and orchestration
```