# Flask API for Telegram Messages - With Persistent Session
# Converts n8n_simple.py to a Flask API

from flask import Flask, request, jsonify
from flask_cors import CORS
from telethon import TelegramClient
import asyncio
import threading
import json
import os

app = Flask(__name__)
CORS(app)  # Allow cross-origin requests

# Telegram credentials
API_ID = 20899105
API_HASH = 'ad33eb9a75b3fe5c4b4c59467641fee9'
PHONE = '+919150557888'

# Session file for persistent storage
SESSION_FILE = 'telegram_api_session'

class TelegramManager:
    def __init__(self):
        self.client = None
        self.loop = None
        self.thread = None
        self.ready = threading.Event()
        self.start_client()
    
    def start_client(self):
        """Start Telegram client in background thread"""
        self.thread = threading.Thread(target=self._run_client, daemon=True)
        self.thread.start()
        self.ready.wait()  # Wait until client is ready
    
    def _run_client(self):
        """Run client in dedicated event loop"""
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        
        # Initialize client with persistent session
        self.client = TelegramClient(SESSION_FILE, API_ID, API_HASH)
        
        # Start client and mark as ready
        self.loop.run_until_complete(self._init_client())
        self.ready.set()
        
        # Keep event loop running
        self.loop.run_forever()
    
    async def _init_client(self):
        """Initialize and start Telegram client"""
        try:
            await self.client.start(phone=PHONE)
            me = await self.client.get_me()
            print(f"✅ Telegram client ready: {me.first_name} ({me.phone})")
        except Exception as e:
            print(f"❌ Failed to start Telegram client: {e}")
            raise
    
    def send_message_sync(self, recipient, message):
        """Send message synchronously"""
        future = asyncio.run_coroutine_threadsafe(
            self._send_message_async(recipient, message), 
            self.loop
        )
        return future.result()
    
    async def _send_message_async(self, recipient, message):
        """Send message asynchronously"""
        try:
            # Try to find recipient
            user = await self.client.get_entity(recipient)
            
            # Send message
            await self.client.send_message(user, message)
            
            return {
                'success': True,
                'status': 'sent',
                'message': f'Message sent to {user.first_name}',
                'recipient': recipient,
                'recipient_name': user.first_name,
                'user_id': user.id
            }
            
        except Exception as e:
            return {
                'success': False,
                'status': 'error',
                'message': str(e),
                'recipient': recipient,
                'solutions': [
                    'Add recipient to your phone contacts',
                    'Ask recipient to message you first',
                    'Use @username instead of phone number'
                ]
            }

# Initialize Telegram manager
print("🚀 Starting Telegram Manager...")
telegram_manager = TelegramManager()

@app.route('/send-message', methods=['POST'])
def send_message():
    """
    Send Telegram message
    
    POST /send-message
    Content-Type: application/json
    
    {
        "mobile_number": "+919003706299",
        "message": "Hello from API!"
    }
    """
    try:
        # Get JSON data
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'error': 'No JSON data provided'
            }), 400
        
        # Extract mobile number and message
        mobile_number = data.get('mobile_number') or data.get('recipient')
        message = data.get('message')
        
        # Validate required fields
        if not mobile_number:
            return jsonify({
                'success': False,
                'error': 'mobile_number field is required'
            }), 400
        
        if not message:
            return jsonify({
                'success': False,
                'error': 'message field is required'
            }), 400
        
        print(f"📨 Sending message to {mobile_number}: {message}")
        
        # Send message
        result = telegram_manager.send_message_sync(mobile_number, message)
        
        # Return result
        status_code = 200 if result['success'] else 400
        return jsonify(result), status_code
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'API Error: {str(e)}'
        }), 500

@app.route('/test', methods=['POST'])
def test_message():
    """
    Send test message to yourself
    
    POST /test
    {
        "message": "Test message (optional)"
    }
    """
    try:
        data = request.get_json() or {}
        test_message = data.get('message', 'Test message from Telegram API! 🧪')
        
        # Send to yourself (your phone number)
        result = telegram_manager.send_message_sync(PHONE, test_message)
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/status', methods=['GET'])
def status():
    """Check API status"""
    session_exists = os.path.exists(f"{SESSION_FILE}.session")
    
    return jsonify({
        'status': 'online',
        'message': 'Telegram Flask API is running',
        'phone': PHONE,
        'session_stored': session_exists,
        'session_file': f"{SESSION_FILE}.session",
        'endpoints': {
            'send_message': 'POST /send-message',
            'test': 'POST /test',
            'status': 'GET /status'
        }
    })

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'Telegram Flask API',
        'session_active': telegram_manager.ready.is_set()
    })

if __name__ == '__main__':
    print("🚀 Starting Telegram Flask API...")
    print("📡 API will be available at: http://localhost:5000")
    print("\n📋 Available endpoints:")
    print("  POST /send-message - Send message to mobile number")
    print("  POST /test - Send test message to yourself")  
    print("  GET /status - Check API status")
    print("  GET /health - Health check")
    print("\n📝 Example usage:")
    print('  curl -X POST http://localhost:5000/send-message \\')
    print('       -H "Content-Type: application/json" \\')
    print('       -d \'{"mobile_number":"+919003706299","message":"Hello!"}\'')
    print(f"\n💾 Session will be stored in: {SESSION_FILE}.session")
    
    app.run(host='0.0.0.0', port=5000, debug=False)