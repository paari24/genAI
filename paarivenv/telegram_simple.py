# Telegram Message Sender - Simple and Reliable Version

from telethon import TelegramClient
import asyncio

# Your credentials
api_id = 20899105
api_hash = 'ad33eb9a75b3fe5c4b4c59467641fee9'
phone = '+919150557888'
recipient_phone = '+919003706299'
message_text = 'Hello! This is a message sent via Telethon from n8n 🎉'

async def main():
    client = TelegramClient('n8n_session', api_id, api_hash)
    
    try:
        await client.start(phone=phone)
        print("✅ Connected to Telegram")
        
        # Test: Send to yourself first
        print("🧪 Testing by sending to yourself...")
        me = await client.get_me()
        await client.send_message(me, f"Test: {message_text}")
        print(f"✅ Test message sent to yourself: {me.first_name}")
        
        # Try multiple methods to find and send to recipient
        user = None
        
        # Method 1: Direct phone lookup
        print(f"🔍 Trying to find user: {recipient_phone}")
        try:
            user = await client.get_entity(recipient_phone)
            print(f"✅ Found user directly: {user.first_name}")
        except Exception as e:
            print(f"❌ Direct lookup failed: {e}")
        
        # Method 2: Try without country code
        if not user:
            try:
                phone_without_plus = recipient_phone.replace('+', '')
                user = await client.get_entity(phone_without_plus)
                print(f"✅ Found user without +: {user.first_name}")
            except Exception as e:
                print(f"❌ Lookup without + failed: {e}")
        
        # Method 3: Try different formats
        if not user:
            formats_to_try = [
                recipient_phone,
                recipient_phone.replace('+', ''),
                recipient_phone.replace('+91', '91'),
                recipient_phone.replace('+91', '+91 '),
            ]
            
            for phone_format in formats_to_try:
                try:
                    print(f"🔍 Trying format: {phone_format}")
                    user = await client.get_entity(phone_format)
                    print(f"✅ Found user with format {phone_format}: {user.first_name}")
                    break
                except:
                    continue
        
        # Send message if user found
        if user:
            await client.send_message(user, message_text)
            print(f"✅ Message sent successfully to {user.first_name}")
        else:
            print("\n❌ Could not find the recipient")
            print("\n💡 SOLUTIONS TO TRY:")
            print("1. 📱 Add the person to your phone contacts first, then sync with Telegram")
            print("2. 💬 Ask them to send you a message first on Telegram") 
            print("3. 👥 Create a group, add both of you, then send there")
            print("4. 🔗 Get their @username and use that instead")
            print("\n🔧 Want to try alternative methods? Check telegram_advanced.py")
            
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
    finally:
        await client.disconnect()
        print("🔌 Disconnected from Telegram")

if __name__ == "__main__":
    asyncio.run(main())