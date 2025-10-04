# SIMPLE N8N TELEGRAM BOT - COPY THIS TO N8N
# Paste this entire code in n8n "Python Code" node

from telethon import TelegramClient
import asyncio

# 🔧 CONFIGURATION - Change these values
API_ID = 20899105
API_HASH = 'ad33eb9a75b3fe5c4b4c59467641fee9'
PHONE = '+919150557888'
RECIPIENT = '+919003706299'  # Phone number or @username
MESSAGE = 'Hello! Automated message from n8n 🤖'

async def send_message():
    client = TelegramClient('n8n_session', API_ID, API_HASH)
    
    try:
        await client.start(phone=PHONE)
        
        # Find recipient
        user = await client.get_entity(RECIPIENT)
        
        # Send message
        await client.send_message(user, MESSAGE)
        
        # Return success for n8n
        return {
            'status': 'success',
            'message': f'Sent to {user.first_name}',
            'recipient': RECIPIENT
        }
        
    except Exception as e:
        # Return error for n8n
        return {
            'status': 'error',
            'message': str(e),
            'recipient': RECIPIENT,
            'fix': 'Add recipient to contacts or use @username'
        }
    finally:
        await client.disconnect()

# Execute and return result for n8n
result = asyncio.run(send_message())
print(result)

# For n8n to use in next nodes:
items = [{'json': result}]