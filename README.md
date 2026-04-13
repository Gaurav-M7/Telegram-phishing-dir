
# 🔐 Telegram Session Manager & Message Reader

<div align="center">

![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)
![Python](https://img.shields.io/badge/python-3.8+-green.svg)
![License](https://img.shields.io/badge/license-MIT-yellow.svg)
![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey.svg)

**A powerful two-part Telegram tool for secure session management and message interaction**

[Features](#-features) • [Installation](#-installation) • [Usage](#-usage) • [Security](#-security) • [Troubleshooting](#-troubleshooting)

</div>

---

## ⚠️ **IMPORTANT SECURITY WARNING**

<div align="center">

### 🚨 READ THIS BEFORE USING 🚨

</div>

> **This tool handles sensitive Telegram session data. Please understand the risks:**
> - Session strings provide **FULL ACCESS** to your Telegram account
> - Anyone with your session string can read messages, send messages, and access contacts
> - **NEVER** share your session string with anyone
> - **NEVER** commit `.env` files or session strings to GitHub
> - Use this tool **ONLY** for legitimate purposes with proper authorization
> - The developer is **NOT RESPONSIBLE** for any misuse of this tool

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [Prerequisites](#-prerequisites)
- [Installation](#-installation)
  - [Windows Installation](#windows-installation)
  - [Linux/macOS Installation](#linuxmacos-installation)
- [Configuration](#-configuration)
  - [Getting API Credentials](#getting-api-credentials)
  - [Creating a Telegram Bot](#creating-a-telegram-bot)
  - [Finding Your Chat ID](#finding-your-chat-id)
- [Usage Guide](#-usage-guide)
  - [Part 1: Session Generator Bot](#part-1-session-generator-bot-modpy)
  - [Part 2: Interactive Client](#part-2-interactive-client-chatpy)
- [Commands Reference](#-commands-reference)
- [File Structure](#-file-structure)
- [Security Best Practices](#-security-best-practices)
- [Troubleshooting](#-troubleshooting)
- [FAQ](#-faq)
- [Legal Disclaimer](#-legal-disclaimer)
- [Contributing](#-contributing)
- [License](#-license)
- [Support](#-support)

---

## 🎯 Overview

This project consists of two complementary tools:

### Part 1: Session Generator Bot (`mod.py`)
A Telegram bot that securely generates session strings through OTP verification, supporting 2FA and automatic backup.

### Part 2: Interactive Client (`chat.py`)
A command-line interface that uses session strings to interact with Telegram, allowing you to read messages, list contacts, and send messages.

---

## ✨ Features

### 🔹 Session Generator Bot
- ✅ **Secure OTP Verification**: Step-by-step phone number verification
- ✅ **2FA Support**: Handles two-factor authentication
- ✅ **Session String Generation**: Creates reusable session strings
- ✅ **Automatic Backup**: Sends session strings to owner's chat
- ✅ **Error Handling**: Graceful handling of API errors and rate limits
- ✅ **Cancel Operation**: Ability to cancel verification at any time
- ✅ **User-Friendly Interface**: Clear step-by-step instructions

### 🔹 Interactive Client
- ✅ **Multiple Access Methods**: Find contacts by phone, username, or ID
- ✅ **Message Reading**: Read recent messages from any contact
- ✅ **Message Sending**: Send messages to any contact
- ✅ **Contact Information**: View contact details including phone numbers
- ✅ **Chat Listing**: List recent chats with participant information
- ✅ **Account Info**: Display your account details
- ✅ **Interactive Menu**: Easy-to-use command-line interface
- ✅ **Error Recovery**: Robust error handling with helpful tips

---

## 📦 Prerequisites

Before installing, ensure you have:

- **Python 3.8 or higher** installed on your system
- **A Telegram account** with an active phone number
- **Internet connection** for API access
- **Basic command-line knowledge**

### Verify Python Installation
```bash
python --version
# Should output: Python 3.8.x or higher
```

---

## 🔧 Installation

### Windows Installation

#### Step 1: Install Python
1. Download Python from [python.org](https://www.python.org/downloads/)
2. Run the installer
3. ✅ **Check**: "Add Python to PATH"
4. Click "Install Now"

#### Step 2: Download the Project
```cmd
# Using Git
git clone https://github.com/yourusername/telegram-session-manager.git
cd telegram-session-manager

# OR download ZIP from GitHub and extract
```

#### Step 3: Create Virtual Environment
```cmd
# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\activate

# You should see (venv) in your terminal prompt
```

#### Step 4: Install Dependencies
```cmd
# Upgrade pip first
python -m pip install --upgrade pip

# Install requirements
pip install -r requirements.txt
```

### Linux/macOS Installation

#### Step 1: Install Python (if needed)
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install python3 python3-pip python3-venv git

# macOS (using Homebrew)
brew install python3 git

# Fedora
sudo dnf install python3 python3-pip python3-virtualenv git
```

#### Step 2: Clone the Repository
```bash
git clone https://github.com/yourusername/telegram-session-manager.git
cd telegram-session-manager
```

#### Step 3: Create Virtual Environment
```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# You should see (venv) in your terminal prompt
```

#### Step 4: Install Dependencies
```bash
# Upgrade pip
pip install --upgrade pip

# Install requirements
pip install -r requirements.txt
```

---

## ⚙️ Configuration

### Getting API Credentials

#### 1. Get API ID and API Hash

1. Go to **[my.telegram.org](https://my.telegram.org)**
2. Log in with your phone number
3. Click on **"API Development Tools"**
4. Fill in the form:
   - **App title**: `Session Manager` (or any name)
   - **Short name**: `sessionmanager` (or any short name)
   - **Platform**: `Desktop`
   - **Description**: `Personal session management tool`
5. Click **"Create Application"**
6. Copy your **API ID** (a number) and **API Hash** (a string)

> 📸 **Screenshot Reference**: You'll see something like:
> ```
> App api_id: 12345678
> App api_hash: a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6
> ```

#### 2. Creating a Telegram Bot

1. Open Telegram and search for **[@BotFather](https://t.me/BotFather)**
2. Start a chat and send `/newbot`
3. Follow the prompts:
   - **Bot Name**: `My Session Manager Bot` (display name)
   - **Bot Username**: `mysessionmanager_bot` (must end with 'bot')
4. After creation, you'll receive:
   ```
   Done! Congratulations on your new bot.
   
   Use this token to access the HTTP API:
   1234567890:ABCdefGHIjklMNOpqrsTUVwxyz-1234567
   
   Keep your token secure and store it safely!
   ```
5. **Copy and save this token** - it's your `BOT_TOKEN`

#### 3. Finding Your Chat ID

**Method 1: Using @userinfobot**
1. Search for **[@userinfobot](https://t.me/userinfobot)** on Telegram
2. Start the bot and send any message
3. You'll receive your information including:
   ```
   Your ID: 123456789
   ```

**Method 2: Using @RawDataBot**
1. Search for **[@RawDataBot](https://t.me/RawDataBot)**
2. Send any message
3. Look for `"id":` in the response

#### 4. Setting Up Environment Variables

1. **Create the `.env` file:**
```bash
# Copy the example file
cp .env.example .env

# OR create it manually
touch .env  # Linux/macOS
type nul > .env  # Windows
```

2. **Edit the `.env` file** with your credentials:
```env
# Telegram API Credentials (from my.telegram.org)
API_ID=12345678
API_HASH=a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6

# Bot Token (from @BotFather)
BOT_TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyz-1234567

# Your Telegram Chat ID (from @userinfobot)
OWNER_CHAT_ID=123456789
```

3. **Verify the configuration:**
```bash
# Check that .env is not tracked by git
git status

# You should NOT see .env in the list of files to commit
```

---

## 🚀 Usage Guide

### Part 1: Session Generator Bot (`mod.py`)

#### Starting the Bot

1. **Activate your virtual environment:**
```bash
# Windows
venv\Scripts\activate

# Linux/macOS
source venv/bin/activate
```

2. **Run the bot:**
```bash
python mod.py
```

You should see:
```
============================================================
TELEGRAM SESSION VERIFICATION BOT
============================================================
Bot Token: 1234567890:...
API ID: 12345678
Owner Chat ID: 123456789
============================================================
Bot starting...
✅ Bot is running!
📱 Go to your bot on Telegram
💡 Send /start to begin
⏸️  Press Ctrl+C to stop
```

#### Using the Bot on Telegram

1. **Find your bot** on Telegram (search for the username you created)
2. **Start the bot** with `/start`
3. **Begin verification** with `/verify`
4. **Follow the prompts:**

```
Step 1: Enter your phone number
Format: +919876543210

Step 2: Enter OTP digits one by one
- You'll receive a 5-digit code
- Enter each digit when prompted

Step 3: Enter 2FA password (if enabled)
- Only required if you have two-factor authentication

Step 4: Receive your session string
- The session string will be sent to the owner's chat
- A confirmation will appear in your chat
```

#### Bot Commands

| Command | Description |
|---------|-------------|
| `/start` | Display welcome message and instructions |
| `/verify` | Start the phone verification process |
| `/cancel` | Cancel the current verification process |
| `/help` | Show available commands and information |

### Part 2: Interactive Client (`chat.py`)

#### Starting the Client

1. **Ensure you have a session string** from Part 1
2. **Run the client:**
```bash
python chat.py
```

3. **Enter your session string when prompted:**
```
Enter your session string: [PASTE YOUR SESSION STRING HERE]
```

4. **Successful connection shows:**
```
🚀 Starting Telegram Client...
✅ Successfully logged in!

==================================================
ACCOUNT INFORMATION
==================================================
👤 Name:    Your Name
🆔 ID:      123456789
📱 Phone:   +919876543210
🔗 Username: @yourusername
🤖 Bot:     No
==================================================
```

#### Interactive Menu Options

##### Option 1: Read Messages by Phone Number
```
📞 READ MESSAGES BY PHONE NUMBER
----------------------------------------
📝 Enter phone number in international format:
   Example: +919876543210 (India)
   Example: +1234567890 (US)
   Example: +447911123456 (UK)
----------------------------------------
Enter phone number: +919876543210
How many recent messages to read? (1-50): 10
```

**What happens:**
- Searches for the contact by phone number
- Displays contact information
- Shows recent messages with timestamps
- Offers option to reply

##### Option 2: Read Messages by Username/ID
```
🔍 READ MESSAGES BY USERNAME OR ID
Enter username (without @) or chat ID: username
How many recent messages to read? (1-50): 10
```

**Use this for:**
- Finding users by their @username
- Accessing group chats by ID
- Reading channel messages by ID

##### Option 3: List Recent Chats
```
📋 LISTING RECENT CHATS
Showing last 10 chats:

👤 Contact Name
   📞 Phone: +919876543210
   🆔 ID: 123456789
   💬 Last msg: 2024-01-15 14:30

👥 Group Name
   🆔 ID: -1001234567890
   👥 Members: 50
   💬 Last msg: 2024-01-15 14:25
```

##### Option 4: Send a Message
```
💬 SEND MESSAGE
You can send to:
1. Phone number (e.g., +919876543210)
2. Username (e.g., username or @username)
3. Chat ID (e.g., 123456789 or -1001234567890)
4. 'me' (to send to yourself)

Enter recipient: +919876543210
Enter your message: Hello! This is a test message.
✅ Message sent successfully!
```

##### Option 5: Check Account Info
Displays your current account information including:
- Name
- User ID
- Phone number
- Username
- Bot status

##### Option 6: Exit
Safely exits the application and disconnects from Telegram.

---

## 📚 Commands Reference

### Bot Commands (in Telegram)

| Command | Description | Example |
|---------|-------------|---------|
| `/start` | Initialize the bot | `/start` |
| `/verify` | Start phone verification | `/verify` |
| `/cancel` | Cancel current operation | `/cancel` |
| `/help` | Show help message | `/help` |

### Terminal Commands

| Command | Description | Platform |
|---------|-------------|----------|
| `python mod.py` | Start the session generator bot | All |
| `python chat.py` | Start the interactive client | All |
| `Ctrl+C` | Stop the running program | All |
| `deactivate` | Exit virtual environment | All |

---

## 📁 File Structure

```
telegram-session-manager/
│
├── 📄 mod.py                    # Session generator bot
├── 📄 chat.py                   # Interactive client
├── 📄 requirements.txt          # Python dependencies
├── 📄 .env.example             # Environment template
├── 📄 .gitignore               # Git ignore rules
├── 📄 README.md                # This documentation
├── 📄 LICENSE                  # MIT License
│
├── 📁 venv/                    # Virtual environment (not in git)
├── 📁 __pycache__/             # Python cache (not in git)
└── 📄 .env                     # Your credentials (not in git)
```

---

## 🔒 Security Best Practices

### ✅ DO's

- **Always use a virtual environment**
- **Keep your `.env` file secure and local**
- **Verify the bot is yours before sharing any OTP**
- **Use strong 2FA passwords**
- **Regularly review active Telegram sessions**
- **Revoke session strings when no longer needed**
- **Keep your API credentials confidential**
- **Update dependencies regularly**

### ❌ DON'Ts

- **NEVER commit `.env` to version control**
- **NEVER share session strings publicly**
- **DON'T use this tool on public computers**
- **DON'T verify others' phone numbers without permission**
- **NEVER bypass Telegram's rate limits intentionally**
- **DON'T use for spam or harassment**
- **DON'T store session strings in plain text files**

### 🔐 Securing Your Session

1. **Check active sessions regularly:**
   - Telegram Settings → Privacy and Security → Active Sessions
   - Terminate any unrecognized sessions

2. **Enable 2FA on your account:**
   - Settings → Privacy and Security → Two-Step Verification
   - Set a strong password and recovery email

3. **Revoke compromised sessions:**
   - If you suspect a session string is compromised
   - Go to Settings → Privacy and Security → Active Sessions
   - Click "Terminate all other sessions"

---

## 🔧 Troubleshooting

### Common Issues and Solutions

#### ❌ Error: `FLOOD_WAIT_X`

**Problem:** Too many verification attempts
**Solution:** 
- Wait for X seconds as specified
- Try again with a longer interval between attempts
- Use a different phone number if possible

#### ❌ Error: `PHONE_NUMBER_INVALID`

**Problem:** Incorrect phone number format
**Solution:**
- Use international format: `+[country_code][number]`
- Example for India: `+919876543210`
- Example for US: `+1234567890`
- Remove any spaces or special characters

#### ❌ Error: `SESSION_PASSWORD_NEEDED`

**Problem:** Account has 2FA enabled
**Solution:**
- Enter your 2FA password when prompted
- If forgotten, you'll need to recover it through Telegram

#### ❌ Error: `API_ID_INVALID`

**Problem:** Incorrect API credentials
**Solution:**
- Verify API_ID and API_HASH from my.telegram.org
- Check that API_ID is a number, not a string
- Ensure no extra spaces in .env file

#### ❌ Error: `ModuleNotFoundError: No module named 'telethon'`

**Problem:** Dependencies not installed
**Solution:**
```bash
# Activate virtual environment
# Windows: venv\Scripts\activate
# Linux/macOS: source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

#### ❌ Error: `ConnectionError: Connection to Telegram failed`

**Problem:** Network or proxy issues
**Solution:**
- Check your internet connection
- Disable VPN/proxy if active
- Try using a different network
- Check if Telegram is blocked in your region

#### ❌ Error: `No contact found with phone: +XXXXXXXXXXX`

**Problem:** Contact not in Telegram or privacy settings
**Solution:**
- Ensure the number is registered on Telegram
- Add the contact to your Telegram contacts first
- Check if the user has hidden their phone number
- Try searching by username instead

#### ❌ Bot not responding

**Problem:** Bot token invalid or bot not started
**Solution:**
- Verify BOT_TOKEN in .env file
- Check if bot is running (`python mod.py`)
- Try `/start` command again
- Revoke and create new bot token from @BotFather

### Debug Mode

To get more detailed error messages:

```python
# Add to top of mod.py and chat.py
import logging
logging.basicConfig(level=logging.DEBUG)
```

---

## ❓ FAQ

### General Questions

**Q: Is this tool legal?**
A: Yes, the tool itself is legal. However, using it to access others' accounts without permission violates Telegram's Terms of Service and potentially local laws.

**Q: Can I run multiple sessions simultaneously?**
A: Yes, each session string can be used independently in different client instances.

**Q: How long do session strings last?**
A: Session strings remain valid until:
- You manually terminate the session
- You change your password
- You enable/disable 2FA
- Telegram detects suspicious activity

**Q: Can I use this on a VPS/cloud server?**
A: Yes, but be aware that Telegram may flag logins from new IP addresses.

### Technical Questions

**Q: Why do I need to enter OTP digits one by one?**
A: This prevents automated bots from intercepting the full OTP, adding a security layer.

**Q: What's the difference between API ID and Bot Token?**
A: 
- API ID/Hash: Identifies your application to Telegram's API
- Bot Token: Authenticates your specific bot instance

**Q: Can I modify the code for my own needs?**
A: Yes! The project is open-source under MIT license.

**Q: Why can't I see someone's phone number even though they're in my contacts?**
A: Telegram privacy settings allow users to hide their phone numbers.

### Security Questions

**Q: Is my phone number safe?**
A: Phone numbers are only used for verification and are not stored permanently.

**Q: Can the bot owner see my messages?**
A: The bot owner receives the session string, which grants access to the account. Only use bots you trust.

**Q: How do I revoke a session string?**
A: Go to Telegram Settings → Privacy and Security → Active Sessions → Terminate the session.

**Q: What happens if I lose my session string?**
A: You can generate a new one using the bot. The old one will still work until terminated.

---

## ⚖️ Legal Disclaimer

### Educational Purpose

This software is provided for **educational and research purposes only**. The developers assume no liability and are not responsible for any misuse or damage caused by this program.

### User Responsibility

By using this software, you agree that:

1. **You will comply with all applicable laws and regulations**
2. **You will respect Telegram's Terms of Service**
3. **You will obtain proper consent before accessing others' data**
4. **You will not use this tool for harassment, spam, or illegal activities**
5. **You are solely responsible for your actions and their consequences**

### Privacy Considerations

- **Respect user privacy**: Only access accounts you own or have explicit permission to access
- **Data protection**: Handle any accessed data in compliance with privacy laws (GDPR, CCPA, etc.)
- **Informed consent**: Users should be aware when their data is being accessed

### Telegram Terms of Service

This tool interacts with Telegram's API. Please review [Telegram's Terms of Service](https://telegram.org/tos) and [API Terms of Service](https://core.telegram.org/api/terms).

---

## 🤝 Contributing

### How to Contribute

We welcome contributions! Here's how:

1. **Fork the repository**
2. **Create a feature branch:**
```bash
git checkout -b feature/amazing-feature
```
3. **Make your changes**
4. **Test thoroughly**
5. **Commit your changes:**
```bash
git commit -m 'Add amazing feature'
```
6. **Push to your branch:**
```bash
git push origin feature/amazing-feature
```
7. **Open a Pull Request**

### Contribution Guidelines

- ✅ Follow PEP 8 style guide
- ✅ Add comments for complex logic
- ✅ Update documentation for new features
- ✅ Test on different platforms if possible
- ✅ Keep security in mind
- ❌ Don't commit sensitive data
- ❌ Don't include compiled files

### Reporting Bugs

When reporting bugs, include:
- Operating system and version
- Python version
- Steps to reproduce
- Expected vs actual behavior
- Error messages (if any)
- Screenshots (if applicable)

### Feature Requests

Open an issue with:
- Clear description of the feature
- Use case/scenario
- Potential implementation approach
- Why it would be valuable

---

## 📄 License

### MIT License

```
Copyright (c) 2024 [Your Name]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

## 📞 Support

### Getting Help

1. **Check Documentation**: This README covers most questions
2. **Search Issues**: [GitHub Issues](https://github.com/yourusername/telegram-session-manager/issues)
3. **Open New Issue**: If your problem isn't already reported

### Community

- **GitHub Discussions**: For general questions and community support
- **Issue Tracker**: For bugs and feature requests

### Contact

For security vulnerabilities or private inquiries:
- EMAIL:

**Note**: Please do not send session strings or sensitive data via email.

---

## 🙏 Acknowledgments

### Libraries Used

- **[python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot)**: Telegram Bot API wrapper
- **[Telethon](https://github.com/LonamiWebs/Telethon)**: MTProto library for Telegram
- **[python-dotenv](https://github.com/theskumar/python-dotenv)**: Environment variable management

### Inspiration

This project was created to simplify Telegram session management while maintaining security best practices.

---

## 📊 Project Status

| Component | Status | Version |
|-----------|--------|---------|
| Session Generator Bot | ✅ Stable | 1.0.0 |
| Interactive Client | ✅ Stable | 1.0.0 |
| Documentation | ✅ Complete | 1.0.0 |

### Roadmap

- [ ] Add message export functionality
- [ ] Support for media downloads
- [ ] Web interface option
- [ ] Multi-account management
- [ ] Scheduled messages

---

<div align="center">

### ⭐ If you found this useful, please star the repository! ⭐

**Made with ❤️ for the Telegram community**

[⬆ Back to Top](#-telegram-session-manager--message-reader)

</div>
```

---

## 📝 Additional Files to Create

### `.env.example` (Complete)
```env
# Telegram API Credentials
# Get these from https://my.telegram.org
API_ID=12345678
API_HASH=your_api_hash_here_32_characters_long

# Bot Token from @BotFather
BOT_TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyz-1234567

# Your Telegram Chat ID
# Get from @userinfobot on Telegram
OWNER_CHAT_ID=123456789
```

### `.gitignore` (Complete)
```gitignore
# Environment variables - NEVER COMMIT THIS!
.env
.env.local
.env.production

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# Virtual Environment
venv/
env/
ENV/
env.bak/
venv.bak/
virtualenv/

# Session files - NEVER COMMIT!
*.session
*.session-journal
session_strings/
*_session.txt

# Logs
*.log
*.log.*
logs/
debug.log

# IDE
.vscode/
.idea/
*.swp
*.swo
*~
.DS_Store

# OS
Thumbs.db
desktop.ini

# Sensitive data
credentials.txt
secrets.json
config.ini

# Backup files
*.bak
*.backup
*.old

# Temporary files
*.tmp
*.temp
temp/
tmp/
```

### `requirements.txt` (Complete with versions)
```txt
# Core dependencies
python-telegram-bot==20.7
python-telegram-bot[job-queue]==20.7
telethon==1.36.0
python-dotenv==1.0.0

# Optional but recommended
cryptg==0.4.0          # Faster encryption for Telethon
aiohttp==3.9.1         # Async HTTP client
aiofiles==23.2.1       # Async file operations

# Development dependencies (optional)
pytest==7.4.4          # Testing framework
black==23.12.1         # Code formatter
flake8==7.0.0          # Linter
mypy==1.8.0           # Static type checker
```

### `LICENSE` File
Create a file named `LICENSE` with the MIT license text from above.

---

## 🚀 Quick Start Scripts

### For Windows (`run.bat`)
```batch
@echo off
echo ========================================
echo Telegram Session Manager
echo ========================================
echo.
echo Choose an option:
echo 1. Run Session Generator Bot
echo 2. Run Interactive Client
echo 3. Install Dependencies
echo 4. Exit
echo.

set /p choice="Enter choice (1-4): "

if "%choice%"=="1" (
    call venv\Scripts\activate
    python mod.py
    pause
) else if "%choice%"=="2" (
    call venv\Scripts\activate
    python chat.py
    pause
) else if "%choice%"=="3" (
    call venv\Scripts\activate
    pip install -r requirements.txt
    pause
) else if "%choice%"=="4" (
    exit
) else (
    echo Invalid choice
    pause
)
```

### For Linux/macOS (`run.sh`)
```bash
#!/bin/bash

echo "========================================"
echo "Telegram Session Manager"
echo "========================================"
echo ""
echo "Choose an option:"
echo "1. Run Session Generator Bot"
echo "2. Run Interactive Client"
echo "3. Install Dependencies"
echo "4. Exit"
echo ""

read -p "Enter choice (1-4): " choice

case $choice in
    1)
        source venv/bin/activate
        python mod.py
        ;;
    2)
        source venv/bin/activate
        python chat.py
        ;;
    3)
        source venv/bin/activate
        pip install -r requirements.txt
        ;;
    4)
        exit 0
        ;;
    *)
        echo "Invalid choice"
        ;;
esac

read -p "Press Enter to continue..."
```

Make the script executable:
```bash
chmod +x run.sh
```

---
