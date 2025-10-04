# Test script for Telegram Flask API
import requests
import json

# API base URL (change this to your ngrok URL when using ngrok)
BASE_URL = "http://localhost:5000"
# For ngrok: BASE_URL = "https://your-ngrok-id.ngrok.io"

def test_status():
    """Test API status"""
    print("🔍 Testing API status...")
    try:
        response = requests.get(f"{BASE_URL}/status")
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
    except Exception as e:
        print(f"❌ Error: {e}")

def test_send_message():
    """Test sending message"""
    print("\n📨 Testing send message...")
    
    data = {
        "mobile_number": "+919003706299",  # Change this to your target number
        "message": "Hello! This is a test message from Flask API 🚀"
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/send-message",
            headers={"Content-Type": "application/json"},
            json=data
        )
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
    except Exception as e:
        print(f"❌ Error: {e}")

def test_self_message():
    """Test sending message to yourself"""
    print("\n🧪 Testing self message...")
    
    data = {
        "message": "Test message to myself from API! 📱"
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/test",
            headers={"Content-Type": "application/json"},
            json=data
        )
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    print("🚀 Testing Telegram Flask API")
    print(f"📡 Base URL: {BASE_URL}")
    print("=" * 50)
    
    # Run tests
    test_status()
    test_self_message()
    test_send_message()
    
    print("\n✅ Testing complete!")
    print("\n💡 To use with ngrok:")
    print("1. Start your Flask API: python telegram_api.py")
    print("2. Start ngrok: ngrok http 5000")
    print("3. Update BASE_URL in this script with your ngrok URL")
    print("4. Run this test script again")