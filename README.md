<!-- Improved compatibility of back to top link: See: https://github.com/othneildrew/Best-README-Template/pull/73 -->
<a id="readme-top"></a>



<!-- PROJECT SHIELDS -->
[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![License][license-shield]][license-url]



<!-- PROJECT LOGO -->
<br />
<div align="center">

<h3 align="center">Email Scraper</h3>

  <p align="center">
    Fetches one sender's emails from Gmail over IMAP and saves each as a .md file with a plain-text body.
    <br />
    <br />
    <a href="https://github.com/davidaparici0/email-scraper/issues/new">Report Bug</a>
    &middot;
    <a href="https://github.com/davidaparici0/email-scraper/issues/new">Request Feature</a>
  </p>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#known-limitations">Known Limitations</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

I built this tool to solve a personal data problem: I subscribe to high-value newsletters but found it difficult to aggregate and analyze the insights programmatically.

Email Scraper signs in to a Gmail account over IMAP, searches All Mail for emails from one sender, and writes each email to a `.md` file named after its subject. Each file holds the subject as a heading, the sender and date, and the body as plain text.

How it works:

1. `src/config.py` reads your settings from a `.env` file and builds an IMAP search for the sender in `TARGET_EMAIL`.
2. `src/client.py` opens an SSL connection to `IMAP_SERVER`, signs in, selects `[Gmail]/All Mail`, runs the search, and downloads each matching email.
3. `src/parser.py` extracts the body text, using Beautiful Soup to turn HTML into plain text. It also builds the file name by deleting the characters `\ / * ? : " < > |` from the subject and replacing spaces with underscores.
4. `src/main.py` runs these steps in order and writes one file per email into `output/`.

Here is example console output from a run, with an invented sender and subjects:

```text
Connected to IMAP server (All Mail).
Searching for: (FROM "newsletter@example.com")
Found 3 emails.
[+] Saved: output/The_Weekly_Byte_Issue_40.md
[+] Saved: output/The_Weekly_Byte_Issue_41.md
[+] Saved: output/The_Weekly_Byte_Issue_42.md
```

And this is `output/The_Weekly_Byte_Issue_42.md`, written from an HTML-only newsletter (a single `text/html` part) that has a heading, a numbered list, and a link:

```markdown
# The Weekly Byte: Issue 42

**Sender:** newsletter@example.com
**Date:** Tue, 08 Sep 2026 14:05:00 +0000

---

This week in backend engineering

Three reads worth your time.

Connection pooling without surprises

Reading query plans

Retry budgets

Read the full issue

Thanks for reading.
```

The heading inside the file keeps the original subject, while the file name drops the colon and uses underscores. The newsletter's heading, list, and link all become plain lines of text, and the link's URL is not kept. If an email also has a plain-text version, both versions are saved and the content appears twice. [Known Limitations](#known-limitations) lists these and the other gaps.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



### Built With

* [![Python][Python-shield]][Python-url]
* [![uv][uv-shield]][uv-url]
* [![Beautiful Soup][BeautifulSoup-shield]][BeautifulSoup-url]
* [![python-dotenv][python-dotenv-shield]][python-dotenv-url]

The IMAP connection and email parsing use `imaplib` and `email` from the Python standard library.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- GETTING STARTED -->
## Getting Started

To run the script on your own machine, you need uv and a personal Gmail account that can use an app password.

### Prerequisites

* uv. If Python 3.14 is not installed, uv downloads it for you. On macOS and Linux, install uv with its installer script. For Windows and other methods, such as Homebrew, see the [uv installation guide](https://docs.astral.sh/uv/getting-started/installation/).
  ```sh
  curl -LsSf https://astral.sh/uv/install.sh | sh
  ```
* A personal Gmail account with 2-Step Verification turned on. The script signs in with a password, not with "Sign in with Google", so it needs an app password, and Google only offers app passwords on accounts with 2-Step Verification. Google may not offer them if 2-Step Verification uses only security keys, if the account has Advanced Protection, or if you are signed in to a work, school, or other organization account. IMAP is always on for personal Gmail accounts, so there is no setting to enable. The script expects the All Mail folder to be named `[Gmail]/All Mail`, which is not the case on every account; see [Known Limitations](#known-limitations).

### Installation

1. Create an app password for your Google account by following Google's [Sign in with app passwords](https://support.google.com/accounts/answer/185833) guide. Google revokes app passwords when you change your account password, so create a new one if you do.
2. Clone the repo
   ```sh
   git clone https://github.com/davidaparici0/email-scraper.git
   cd email-scraper
   ```
3. Install the dependencies into `.venv`
   ```sh
   uv sync
   ```
4. Create a file named `.env` in the repository root with these four settings. Replace the example values with your Gmail address, the app password from step 1, and the sender whose emails you want to save. `.env` is listed in `.gitignore`, so git will not pick it up by accident.
   ```ini
   EMAIL_USER=you@gmail.com
   EMAIL_PASSWORD=abcdefghijklmnop
   IMAP_SERVER=imap.gmail.com
   TARGET_EMAIL=newsletter@example.com
   ```
   * `EMAIL_USER` is the Gmail address to sign in with.
   * `EMAIL_PASSWORD` is the app password from step 1, not your normal Google password. If Google shows it in groups separated by spaces, leave the spaces out.
   * `IMAP_SERVER` is `imap.gmail.com`. The script does not check that it is set before connecting.
   * `TARGET_EMAIL` is the sender to search for. If the line is missing, the script searches for `default@example.com`. Do not leave the value blank: the script then searches for an empty sender, which under the IMAP standard can match every email in All Mail.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- USAGE EXAMPLES -->
## Usage

From the repository root, run:

```sh
uv run -m src.main
```

The script creates `output/` in the current directory if it does not exist, writes one `.md` file per matching email into it, and prints a line for each file it saves, as in the example under [About The Project](#about-the-project). `output/` is listed in `.gitignore`, so git will not pick up the saved emails by accident.

* To save emails from a different sender, change `TARGET_EMAIL` in `.env` and run the command again.
* Every run downloads all matching emails again and overwrites files that have the same name.
* Running the script can mark the downloaded emails as read. See [Known Limitations](#known-limitations).
* If `EMAIL_USER` or `EMAIL_PASSWORD` is missing, the script stops with `ValueError: Missing EMAIL_USER or EMAIL_PASSWORD in .env file`.
* If signing in fails, the script prints `Connection failed:` followed by the error, then stops with a Python traceback.
* If the script cannot reach the server, for example because `IMAP_SERVER` is missing or wrong, it stops with a Python traceback and does not print `Connection failed:`.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- KNOWN LIMITATIONS -->
## Known Limitations

* **Gmail only, and only when All Mail is named `[Gmail]/All Mail`.** The mailbox name is hard-coded, and some Gmail accounts use a different one: Google's documentation mentions a `[GoogleMail]` prefix, and folder names can be translated into the account's language. When the mailbox cannot be selected, on those accounts or with other providers, the script still prints `Connected to IMAP server (All Mail).` and then stops with an error that begins `command SEARCH illegal in state AUTH`.
* **One sender per run.** `TARGET_EMAIL` is a single value, used in one IMAP `FROM` search.
* **`IMAP_SERVER` is not validated.** Only `EMAIL_USER` and `EMAIL_PASSWORD` are checked at startup, but the script cannot connect without `IMAP_SERVER`.
* **The server's certificate is not checked.** The IMAP connection is encrypted, but it is opened without certificate or host-name verification, so the script does not confirm that it has reached the real server before it sends your app password.
* **The body is plain text, not Markdown.** Headings and lists lose their formatting, and link URLs are dropped. A link, bold or italic text, or a styled span in the middle of a sentence splits the sentence across lines. Image alt text is dropped, text hidden with CSS (such as preview text) is kept, and the HTML page title, if the email has one, is added at the top of the body.
* **Multipart emails can repeat text or include attachments.** Every `text/plain` part and every `text/html` part is written, so an email that has both a plain-text and an HTML version contains its text twice, and text and HTML attachments are added to the body. The parts are joined with nothing between them, so the end of one part can run into the start of the next.
* **Character sets in bodies are ignored.** Bodies are decoded as UTF-8 and bytes that do not decode are dropped, so `café` in a Latin-1 email is saved as `caf`.
* **Some subjects stop the run or break the file name.**
  * An email with no `Subject` header, a subject Python cannot decode (for example raw non-ASCII bytes, or bytes that do not match the declared character set), or a subject too long to use as a file name raises an error and stops the run. Emails after it are not saved.
  * A subject that mixes encoded and plain text keeps only its first part, so a subject that shows as `Café weekly digest` can be saved as `Café`.
  * A long plain-text subject that is folded over several header lines keeps its line break, which ends up in the file name and splits the heading inside the file.
* **Sender and date are copied as they are.** The `From` and `Date` headers are not decoded, so a sender name with non-ASCII characters appears in its encoded form (such as `=?utf-8?q?...?=`), and a header folded over several lines keeps its line break.
* **Files can be overwritten.** File names come from the subject alone, so a later email whose subject produces the same file name replaces the earlier file. That includes subjects that differ only in removed characters, or only in letter case on a case-insensitive file system such as the macOS default. An email with an empty subject, or a subject made only of removed characters, is saved as `.md`, a hidden file that each such email overwrites.
* **No incremental runs.** Every run downloads all matching emails again.
* **Fetched emails can be marked as read.** The mailbox is opened read-write and each email is fetched with `RFC822`, which under the IMAP standard (RFC 3501) sets the `\Seen` flag.
* **No logging, tests, or CI.** Progress is reported with `print()` only.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- ROADMAP -->
## Roadmap

- [ ] Better output files
    - [ ] Real Markdown that keeps headings, lists, link URLs, and whole sentences
    - [ ] One body per email, preferring the HTML part when both are present and leaving out attachments
    - [ ] Decoding that uses each email's declared character set
    - [ ] Unique file names of a safe length, for example prefixed with the email's date
- [ ] Reliable decoding of subject, sender, and date headers, including missing, folded, and partly encoded ones
- [ ] Skip an email that cannot be processed instead of stopping the run
- [ ] Incremental runs that skip emails already saved
- [ ] Read-only mailbox access, so running the script does not change read status
- [ ] Certificate and host-name verification for the IMAP connection
- [ ] Several senders in one run
- [ ] Other IMAP providers, and Gmail accounts whose All Mail folder has a different name
- [ ] Startup checks for every required setting
- [ ] Logging, tests, and CI

See [Known Limitations](#known-limitations) for what the current version does not handle, and the [issues page](https://github.com/davidaparici0/email-scraper/issues) to propose features or report bugs.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- LICENSE -->
## License

Distributed under the MIT License. See [`LICENSE.txt`][license-url] for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTACT -->
## Contact

Project Link: [https://github.com/davidaparici0/email-scraper](https://github.com/davidaparici0/email-scraper)

Issues: [https://github.com/davidaparici0/email-scraper/issues](https://github.com/davidaparici0/email-scraper/issues)

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

* [Best-README-Template](https://github.com/othneildrew/Best-README-Template)
* [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/)
* [python-dotenv](https://github.com/theskumar/python-dotenv)
* [uv](https://github.com/astral-sh/uv)
* [Shields.io](https://shields.io)

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- MARKDOWN LINKS & IMAGES -->
[contributors-shield]: https://img.shields.io/github/contributors/davidaparici0/email-scraper.svg?style=for-the-badge
[contributors-url]: https://github.com/davidaparici0/email-scraper/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/davidaparici0/email-scraper.svg?style=for-the-badge
[forks-url]: https://github.com/davidaparici0/email-scraper/network/members
[stars-shield]: https://img.shields.io/github/stars/davidaparici0/email-scraper.svg?style=for-the-badge
[stars-url]: https://github.com/davidaparici0/email-scraper/stargazers
[issues-shield]: https://img.shields.io/github/issues/davidaparici0/email-scraper.svg?style=for-the-badge
[issues-url]: https://github.com/davidaparici0/email-scraper/issues
[license-shield]: https://img.shields.io/github/license/davidaparici0/email-scraper.svg?style=for-the-badge
[license-url]: https://github.com/davidaparici0/email-scraper/blob/main/LICENSE.txt
[Python-shield]: https://img.shields.io/badge/Python-3.14-3776AB?style=for-the-badge&logo=python&logoColor=white
[Python-url]: https://www.python.org/
[uv-shield]: https://img.shields.io/badge/uv-DE5FE9?style=for-the-badge&logo=uv&logoColor=white
[uv-url]: https://docs.astral.sh/uv/
[BeautifulSoup-shield]: https://img.shields.io/badge/Beautiful_Soup-4.14-59666C?style=for-the-badge
[BeautifulSoup-url]: https://www.crummy.com/software/BeautifulSoup/
[python-dotenv-shield]: https://img.shields.io/badge/python--dotenv-1.2-555555?style=for-the-badge
[python-dotenv-url]: https://github.com/theskumar/python-dotenv
