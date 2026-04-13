import asyncio
from telethon import TelegramClient
from telethon.sessions import StringSession
from telethon.tl.types import InputPhoneContact
from telethon.tl.functions.contacts import ImportContactsRequest
import re

class InteractiveTelegramClient:
    def __init__(self):
        self.api_id = 
        self.api_hash = ""
        self.session_string = ""
        self.client = None
    
    async def start(self):
        """Start the interactive client"""
        print("🚀 Starting Telegram Client...")
        
        try:
            # Create client with session
            self.client = TelegramClient(
                StringSession(self.session_string),
                self.api_id,
                self.api_hash
            )
            
            # Connect
            await self.client.connect()
            
            # Check authorization
            if not await self.client.is_user_authorized():
                print("❌ Session invalid or expired")
                return False
            
            print("✅ Successfully logged in!")
            
            # Show account info
            await self.show_account_info()
            
            # Start interactive menu
            await self.interactive_menu()
            
            return True
            
        except Exception as e:
            print(f"❌ Error: {e}")
            return False
    
    async def show_account_info(self):
        """Display account information"""
        me = await self.client.get_me()
        
        print("\n" + "=" * 50)
        print("ACCOUNT INFORMATION")
        print("=" * 50)
        print(f"👤 Name:    {me.first_name or ''} {me.last_name or ''}")
        print(f"🆔 ID:      {me.id}")
        print(f"📱 Phone:   {me.phone}")
        print(f"🔗 Username: @{me.username}" if me.username else "🔗 Username: Not set")
        print(f"🤖 Bot:     {'Yes' if me.bot else 'No'}")
        print("=" * 50)
    
    async def get_contact_by_phone(self, phone_number):
        """Find contact by phone number"""
        try:
            # Clean the phone number
            phone_number = self.clean_phone_number(phone_number)
            
            if not phone_number.startswith('+'):
                phone_number = '+' + phone_number
            
            print(f"🔍 Searching for contact with phone: {phone_number}")
            
            # Try to get the contact directly
            try:
                # First, check if it's in our contacts
                contacts = await self.client.get_contacts()
                for contact in contacts:
                    if hasattr(contact, 'phone') and contact.phone:
                        if self.normalize_phone(contact.phone) == self.normalize_phone(phone_number):
                            print(f"✅ Found in contacts: {contact.first_name}")
                            return contact
            except:
                pass
            
            # Try to import as contact to get user info
            try:
                contact = InputPhoneContact(
                    client_id=0,
                    phone=phone_number,
                    first_name="Temp",
                    last_name="Contact"
                )
                
                result = await self.client(ImportContactsRequest([contact]))
                
                if result.users:
                    user = result.users[0]
                    print(f"✅ Found user: {user.first_name or ''} {user.last_name or ''}")
                    
                    # Delete the temporary contact
                    try:
                        await self.client.delete_contacts([user])
                    except:
                        pass
                    
                    return user
            except Exception as e:
                print(f"⚠️ Could not import contact: {e}")
            
            # Try to search in dialogs
            print("🔍 Searching in your chats...")
            async for dialog in self.client.iter_dialogs(limit=100):
                if dialog.is_user:
                    try:
                        entity = await self.client.get_entity(dialog.entity)
                        if hasattr(entity, 'phone') and entity.phone:
                            if self.normalize_phone(entity.phone) == self.normalize_phone(phone_number):
                                print(f"✅ Found in chats: {entity.first_name}")
                                return entity
                    except:
                        continue
            
            # Last resort: try to get entity directly (might work for saved contacts)
            try:
                entity = await self.client.get_entity(phone_number)
                if entity:
                    print(f"✅ Found: {getattr(entity, 'first_name', 'Unknown')}")
                    return entity
            except Exception as e:
                print(f"⚠️ Could not find directly: {e}")
            
            return None
            
        except Exception as e:
            print(f"❌ Error finding contact: {e}")
            return None
    
    def clean_phone_number(self, phone):
        """Clean phone number - remove spaces, dashes, etc."""
        # Remove all non-digit characters except plus sign
        phone = re.sub(r'[^\d+]', '', phone)
        return phone
    
    def normalize_phone(self, phone):
        """Normalize phone number for comparison"""
        phone = self.clean_phone_number(str(phone))
        # Remove leading zeros and country code markers for comparison
        phone = phone.lstrip('+').lstrip('0')
        return phone
    
    async def get_last_messages_by_phone(self, phone_number, limit=10):
        """Get last N messages from a contact by phone number"""
        print(f"\n📱 Searching for contact with phone: {phone_number}")
        
        # Find the contact
        contact = await self.get_contact_by_phone(phone_number)
        
        if not contact:
            print(f"❌ No contact found with phone: {phone_number}")
            print("\n💡 Tips:")
            print("1. Make sure the phone number is in international format (+919876543210)")
            print("2. The contact must be in your Telegram contacts")
            print("3. Try adding the contact to Telegram first")
            return []
        
        contact_name = getattr(contact, 'first_name', '') + ' ' + getattr(contact, 'last_name', '')
        contact_name = contact_name.strip() or 'Unknown'
        
        print(f"\n✅ Contact found: {contact_name}")
        print(f"📞 Phone: {getattr(contact, 'phone', 'Not available')}")
        
        # Get messages
        print(f"\n📨 Getting last {limit} messages...")
        
        try:
            messages = []
            async for message in self.client.iter_messages(contact.id, limit=limit):
                msg_info = {
                    'id': message.id,
                    'date': message.date.strftime('%Y-%m-%d %H:%M:%S') if message.date else 'Unknown',
                    'sender': 'You' if message.out else contact_name,
                    'text': message.text or '[Media or Service Message]',
                    'out': message.out,
                    'media': bool(message.media),
                    'reply_to': message.reply_to.reply_to_msg_id if message.reply_to else None
                }
                messages.append(msg_info)
            
            return messages, contact_name
            
        except Exception as e:
            print(f"❌ Error getting messages: {e}")
            return [], contact_name
    
    async def interactive_menu(self):
        """Interactive menu for user actions"""
        while True:
            print("\n" + "=" * 60)
            print("📱 MAIN MENU")
            print("=" * 60)
            print("1. 📞 Read messages by phone number")
            print("2. 🔍 Read messages by username/ID")
            print("3. 📋 List recent chats")
            print("4. 📨 Send a message")
            print("5. 👤 Check my info")
            print("6. 🚪 Exit")
            print("=" * 60)
            
            try:
                choice = input("\nSelect option (1-6): ").strip()
                
                if choice == '1':
                    await self.read_by_phone_number()
                elif choice == '2':
                    await self.read_by_username_or_id()
                elif choice == '3':
                    await self.list_recent_chats()
                elif choice == '4':
                    await self.send_message()
                elif choice == '5':
                    await self.show_account_info()
                elif choice == '6':
                    print("👋 Goodbye!")
                    break
                else:
                    print("❌ Invalid choice")
                    
            except KeyboardInterrupt:
                print("\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"❌ Error: {e}")
    
    async def read_by_phone_number(self):
        """Read messages by entering phone number"""
        print("\n📞 READ MESSAGES BY PHONE NUMBER")
        print("-" * 40)
        print("📝 Enter phone number in international format:")
        print("   Example: +919876543210 (India)")
        print("   Example: +1234567890 (US)")
        print("   Example: +447911123456 (UK)")
        print("-" * 40)
        
        phone_number = input("\nEnter phone number: ").strip()
        
        if not phone_number:
            print("❌ No phone number entered")
            return
        
        # Ask how many messages to read
        try:
            limit = int(input("How many recent messages to read? (1-50): ").strip())
            if not 1 <= limit <= 50:
                print("❌ Please enter between 1 and 50")
                return
        except ValueError:
            print("❌ Please enter a valid number")
            return
        
        # Get messages
        messages, contact_name = await self.get_last_messages_by_phone(phone_number, limit)
        
        if not messages:
            print(f"\n❌ No messages found with {phone_number}")
            return
        
        print(f"\n{'═'*70}")
        print(f"📨 LAST {len(messages)} MESSAGES WITH {contact_name}")
        print(f"📞 Phone: {phone_number}")
        print(f"{'═'*70}")
        
        if len(messages) == 0:
            print("No messages found.")
            return
        
        for i, msg in enumerate(reversed(messages), 1):
            print(f"\nMessage #{i}")
            print(f"{'─'*45}")
            print(f"📅 Date: {msg['date']}")
            print(f"👤 From: {msg['sender']}")
            print(f"📝 Content: {msg['text'][:300]}{'...' if len(msg['text']) > 300 else ''}")
            if msg['media']:
                print(f"🖼️  Contains media")
            if msg['reply_to']:
                print(f"↩️  Reply to message #{msg['reply_to']}")
            print(f"{'─'*45}")
        
        # Ask if user wants to send a message
        send_msg = input(f"\n💬 Send a message to {contact_name}? (y/n): ").strip().lower()
        if send_msg == 'y':
            message_text = input("Enter your message: ").strip()
            if message_text:
                try:
                    await self.client.send_message(phone_number, message_text)
                    print("✅ Message sent successfully!")
                except Exception as e:
                    print(f"❌ Failed to send: {e}")
    
    async def read_by_username_or_id(self):
        """Read messages by username or ID"""
        print("\n🔍 READ MESSAGES BY USERNAME OR ID")
        
        identifier = input("Enter username (without @) or chat ID: ").strip()
        
        if not identifier:
            print("❌ No identifier entered")
            return
        
        # Add @ if not present for username
        if not identifier.startswith('@') and not identifier.lstrip('-').isdigit():
            identifier = '@' + identifier
        
        # Ask how many messages to read
        try:
            limit = int(input("How many recent messages to read? (1-50): ").strip())
            if not 1 <= limit <= 50:
                print("❌ Please enter between 1 and 50")
                return
        except ValueError:
            print("❌ Please enter a valid number")
            return
        
        try:
            # Get the entity
            entity = await self.client.get_entity(identifier)
            
            entity_name = getattr(entity, 'first_name', getattr(entity, 'title', 'Unknown'))
            
            print(f"\n✅ Found: {entity_name}")
            if hasattr(entity, 'phone'):
                print(f"📞 Phone: {entity.phone}")
            if hasattr(entity, 'username'):
                print(f"🔗 Username: @{entity.username}")
            
            # Get messages
            print(f"\n📨 Getting last {limit} messages...")
            
            messages = []
            async for message in self.client.iter_messages(entity.id, limit=limit):
                sender_name = "You" if message.out else entity_name
                if not message.out and message.sender_id:
                    try:
                        sender = await self.client.get_entity(message.sender_id)
                        sender_name = getattr(sender, 'first_name', getattr(sender, 'title', 'Unknown'))
                    except:
                        pass
                
                msg_info = {
                    'id': message.id,
                    'date': message.date.strftime('%Y-%m-%d %H:%M:%S') if message.date else 'Unknown',
                    'sender': sender_name,
                    'text': message.text or '[Media or Service Message]',
                    'out': message.out,
                    'media': bool(message.media),
                    'reply_to': message.reply_to.reply_to_msg_id if message.reply_to else None
                }
                messages.append(msg_info)
            
            if not messages:
                print("❌ No messages found")
                return
            
            print(f"\n{'═'*70}")
            print(f"📨 LAST {len(messages)} MESSAGES WITH {entity_name}")
            print(f"{'═'*70}")
            
            for i, msg in enumerate(reversed(messages), 1):
                print(f"\nMessage #{i}")
                print(f"{'─'*45}")
                print(f"📅 Date: {msg['date']}")
                print(f"👤 From: {msg['sender']}")
                print(f"📝 Content: {msg['text'][:300]}{'...' if len(msg['text']) > 300 else ''}")
                if msg['media']:
                    print(f"🖼️  Contains media")
                if msg['reply_to']:
                    print(f"↩️  Reply to message #{msg['reply_to']}")
                print(f"{'─'*45}")
            
            # Ask if user wants to send a message
            send_msg = input(f"\n💬 Send a message to {entity_name}? (y/n): ").strip().lower()
            if send_msg == 'y':
                message_text = input("Enter your message: ").strip()
                if message_text:
                    try:
                        await self.client.send_message(entity.id, message_text)
                        print("✅ Message sent successfully!")
                    except Exception as e:
                        print(f"❌ Failed to send: {e}")
            
        except Exception as e:
            print(f"❌ Error: {e}")
            print("\n💡 Tips:")
            print("1. For usernames: Enter without @ (e.g., 'username' not '@username')")
            print("2. For chat IDs: Enter the numeric ID (e.g., -1001234567890 for groups)")
            print("3. Make sure you have the correct username/ID")
    
    async def list_recent_chats(self):
        """List recent chats with phone numbers if available"""
        print("\n📋 LISTING RECENT CHATS")
        
        try:
            limit = 10
            print(f"Showing last {limit} chats:\n")
            
            async for dialog in self.client.iter_dialogs(limit=limit):
                try:
                    entity = await self.client.get_entity(dialog.entity)
                    
                    # Get chat type emoji
                    if dialog.is_user:
                        type_emoji = "👤"
                        chat_name = f"{entity.first_name or ''} {entity.last_name or ''}".strip()
                        phone = getattr(entity, 'phone', 'N/A')
                        print(f"{type_emoji} {chat_name}")
                        if phone and phone != 'N/A':
                            print(f"   📞 Phone: {phone}")
                        print(f"   🆔 ID: {entity.id}")
                        
                    elif dialog.is_group:
                        type_emoji = "👥"
                        chat_name = getattr(entity, 'title', 'Unknown Group')
                        print(f"{type_emoji} {chat_name}")
                        print(f"   🆔 ID: {entity.id}")
                        if hasattr(entity, 'participants_count'):
                            print(f"   👥 Members: {entity.participants_count}")
                            
                    elif dialog.is_channel:
                        type_emoji = "📢"
                        chat_name = getattr(entity, 'title', 'Unknown Channel')
                        print(f"{type_emoji} {chat_name}")
                        print(f"   🆔 ID: {entity.id}")
                        if hasattr(entity, 'username'):
                            print(f"   🔗 @{entity.username}")
                    
                    if dialog.unread_count > 0:
                        print(f"   🔔 Unread: {dialog.unread_count}")
                    
                    print(f"   💬 Last msg: {dialog.message.date.strftime('%Y-%m-%d %H:%M') if hasattr(dialog.message, 'date') else 'Unknown'}")
                    print()
                    
                except Exception as e:
                    print(f"⚠️ Could not get info for {dialog.name}: {str(e)[:50]}")
                    print()
            
        except Exception as e:
            print(f"❌ Error: {e}")
    
    async def send_message(self):
        """Send a message to a chat"""
        print("\n💬 SEND MESSAGE")
        print("You can send to:")
        print("1. Phone number (e.g., +919876543210)")
        print("2. Username (e.g., username or @username)")
        print("3. Chat ID (e.g., 123456789 or -1001234567890)")
        print("4. 'me' (to send to yourself)")
        
        recipient = input("\nEnter recipient: ").strip()
        
        if not recipient:
            print("❌ No recipient specified")
            return
        
        message = input("Enter your message: ").strip()
        
        if not message:
            print("❌ No message specified")
            return
        
        try:
            # Send message
            await self.client.send_message(recipient, message)
            print("✅ Message sent successfully!")
        except Exception as e:
            print(f"❌ Failed to send: {e}")
            print("\n💡 Tips:")
            print("1. For phone numbers: Use international format (+919876543210)")
            print("2. For usernames: Make sure the user exists and you can message them")
            print("3. For chat IDs: Make sure you have the correct ID")

async def main():
    client = InteractiveTelegramClient()
    await client.start()

if __name__ == '__main__':
    asyncio.run(main())
