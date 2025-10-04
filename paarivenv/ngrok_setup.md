# Ngrok Setup for Telegram Flask API

## Step 1: Install ngrok
1. Download ngrok from: https://ngrok.com/download
2. Extract and add to PATH, or run from extracted folder

## Step 2: Start your Flask API
```bash
# In terminal 1 (with virtual environment activated)
cd E:\genAI\genAI\paarivenv
.\paarivenvv\Scripts\activate
python telegram_api.py
```

## Step 3: Start ngrok tunnel
```bash
# In terminal 2
ngrok http 5000
```

## Step 4: Get your public URL
After running ngrok, you'll see something like:
```
Forwarding    https://abc123.ngrok.io -> http://localhost:5000
```

## Step 5: Test your API through ngrok

### Send Message:
```bash
curl -X POST https://YOUR-NGROK-URL.ngrok.io/send-message \
     -H "Content-Type: application/json" \
     -d '{
       "mobile_number": "+919003706299",
       "message": "Hello from ngrok!"
     }'
```

### Test Message (to yourself):
```bash
curl -X POST https://YOUR-NGROK-URL.ngrok.io/test \
     -H "Content-Type: application/json" \
     -d '{
       "message": "Test from ngrok!"
     }'
```

### Check Status:
```bash
curl https://YOUR-NGROK-URL.ngrok.io/status
```

## Step 6: Use in n8n or other applications

### n8n HTTP Request Node:
- Method: POST
- URL: https://YOUR-NGROK-URL.ngrok.io/send-message
- Headers: Content-Type: application/json
- Body:
```json
{
  "mobile_number": "{{$json.phone}}",
  "message": "{{$json.message}}"
}
```

### JavaScript/Postman Example:
```javascript
fetch('https://YOUR-NGROK-URL.ngrok.io/send-message', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    mobile_number: '+919003706299',
    message: 'Hello from web!'
  })
})
.then(response => response.json())
.then(data => console.log(data));
```

## Security Notes:
- ngrok free tier exposes your API publicly
- Consider adding authentication for production use
- Your Telegram session is stored locally and secure

## Troubleshooting:
- Make sure Flask API is running on port 5000
- Check ngrok dashboard at http://127.0.0.1:4040
- Verify your virtual environment is activated