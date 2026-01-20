
![Image alt](https://github.com/kostiakova/petsitting24/blob/main/petsitting24.ch.png)


# petsitting24
Automated selenium parser for site Petsitting24.ch
🐾 PetSitting24.ch

Bot PetSitting24 is an automated Selenium-based scraper designed to monitor new pet-sitting job postings on petsitting24.ch. The bot sends instant Telegram notifications for new offers, including cropped screenshots of the most relevant details.

✨ Key Features

Automated Monitoring: Periodically checks the website for new job offers without manual intervention.

Deduplication Logic: Tracks processed offers via used_links.txt to ensure you never receive the same notification twice.

Visual Summaries: Automatically captures and crops screenshots of key sections (Location, Species, Description) for quick evaluation.

Headless Operation: Runs in a specialized "new-headless" mode, making it perfect for deployment on VPS or home servers.

Telegram Integration: Detailed alerts sent directly to your chosen chat or channel.

📋 Requirements

To run this bot, you will need:

Python 3.13+

Google Chrome (Stable version)

ChromeDriver (Matching your Chrome version)

A registered account on petsitting24.ch

🚀 Installation

```bash
Clone the repository:
git clone [https://github.com/kostiakova/petsitting24.git](https://github.com/kostiakova/petsitting24.git)
&& 
cd petsitting24
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Dependencies include: selenium, pyTelegramBotAPI, python-dotenv, and Pillow.

Environment Setup:
Create a .env file in the root directory:

```python
PET_SITTING_EMAIL=your_email@example.com


PET_SITTING_PASSWORD=your_password


TELEGRAM_BOT_TOKEN=123456789:ABCDefGhIJKlmNoPQRstUV
```

⚙️ Configuration

You can fine-tune the bot's behavior directly in bot.py:

CHAT_ID: Your Telegram User ID or Channel ID (e.g., -100...).

MINUTES_TO_SLEEP: The interval between checks (default: 12 minutes).

FOLDER_SCREENSHOTS: Directory where temporary images are stored.

BINARY_LOC: Path to your Chrome binary (essential for Linux environments).

🛠️ Usage

Simply start the script:

```bash
python auto_find.py
```


How it works:

Initialization: Starts a headless Chrome instance.

Authentication: Logs into your Petsitting24 account.

Search: Navigates to the pet-sitting search page and applies your preferred radius.

Filter: Identifies new links not present in used_links.txt.

Processing: For every new link, it navigates to the profile, extracts text data, and takes screenshots of specific page elements.

Notification: Sends a media group to Telegram containing the data and images.

Idle: Shuts down the driver and sleeps for the configured duration to avoid IP bans.

⚠️ Important Notes

Security: Never commit your .env file to a public repository. It contains sensitive credentials.

Rate Limiting: To avoid being flagged as a bot, do not set the MINUTES_TO_SLEEP too low. The default 12 minutes is generally considered safe.

Legal: This tool is for personal use. Ensure you comply with the website's Terms of Service.

📄 License

This project is licensed under the MIT License - see the LICENSE file for details.  
