# Telegram Data Scraper

A high-performance **Telegram Userbot** built with Python and **Telethon**. It queries the Telegram contacts directory via `ResolvePhoneRequest` to resolve phone numbers into full user profiles (Peer ID, Name, Username, Bio) and maintains a persistent, clean text activity log.

---

## Features

- **Direct Phone Lookup:** Uses Telegram's `ResolvePhoneRequest` to look up accounts linked to specific phone numbers via the contacts directory.
- **Detailed Profile Extraction:** Fetches peer ID, name, username, and profile bio.
- **Persistent Text Logging (`bot_activity.log`):** Records incoming commands, timestamps, sender details, and lookup success/failure states in a readable text file.
- **Lightweight:** No database required; only Telethon.
- **Clean CLI Output:** Real-time event tracking in your terminal.

---

## Prerequisites

- **Python 3.8+**
- A **Telegram API ID and API Hash** from [my.telegram.org](https://my.telegram.org) (log in → *API development tools* → create an app).

---

## Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/YOUR_USERNAME/telegram_data_scraper.git
   cd telegram_data_scraper
   ```

2. **Install dependencies:**
   ```bash
   pip install telethon
   ```

3. **Add your credentials:**
   Open `userinfobot.py` and replace the placeholders with your real values:
   ```python
   API_ID = 1234567                 # your integer API ID
   API_HASH = "your_api_hash_here"  # your API hash string
   ```
   Save the file.

4. **Run the userbot:**
   ```bash
   python userinfobot.py
   ```
   On the first run, Telethon asks for your phone number and login code in the terminal to create a local session file (`lookup_session.session`).

---

## Usage

With the userbot running, send this message in any Telegram chat your account can access:

```text
/lookup +<country code><number>
```

Example:

```text
/lookup +919999999999
```

The bot replies with:

- Peer ID (User ID)
- Name
- Username
- Bio
- Phone number

Every request and result is also saved to `bot_activity.log`.

> **Note:** Results depend on the target's Telegram privacy settings. If a user has restricted who can find them by phone number, the lookup will fail or return nothing.

---

## Project Structure

```text
├── userinfobot.py     # Main script: event handlers and Telegram client logic
├── bot_activity.log   # Auto-generated log of commands, successes, and errors
├── LICENSE            # MIT License
└── README.md          # Project documentation
```

---

## Security Warning ⚠️

- **Never share or commit your `.session` file**, `API_ID`, or `API_HASH`. The included `.gitignore` excludes session files and logs.
- This project runs as a **Userbot** using your personal account session. Keep credentials secure and follow Telegram's [Terms of Service](https://telegram.org/tos) and [API Terms](https://core.telegram.org/api/terms). Excessive lookups can get your account limited or banned.

## Responsible Use

Only look up numbers you have a legitimate reason to, and respect people's privacy and the laws that apply to you. `bot_activity.log` stores personal data; protect it and delete it when no longer needed.

---

## License

Distributed under the MIT License. See `LICENSE` for details.
