# Telegram Session Manager & Message Reader

A two-part Telegram tool for secure session management and message reading.

## ⚠️ Security Warning
- **NEVER** share your session strings
- Session strings give FULL access to your Telegram account
- Keep your `.env` file secure and never commit it
- Use this tool responsibly and ethically

## 🚀 Features

### Part 1: Session Generator Bot (`mod.py`)
- Secure OTP verification
- 2FA support
- Session string generation
- Automatic backup to owner

### Part 2: Interactive Client (`chat.py`)
- Read messages by phone number
- Read messages by username/ID
- List recent chats with phone numbers
- Send messages
- View account information

## 📦 Installation

1. Clone the repository
```bash
git clone https://github.com/yourusername/your-repo.git
cd your-repo
