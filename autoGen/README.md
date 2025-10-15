<div align="center">

# 🤖✨ AutoGen Google Calendar Assistant

<img src="https://img.shields.io/badge/Python-3.8+-blue.svg" alt="Python Version">
<img src="https://img.shields.io/badge/AutoGen-Latest-green.svg" alt="AutoGen">
<img src="https://img.shields.io/badge/Google_Calendar-API-red.svg" alt="Google Calendar">
<img src="https://img.shields.io/badge/AI-Powered-purple.svg" alt="AI Powered">

### *Your AI-Powered Calendar Management Solution* 📅

[Features](#-features) • [Quick Start](#-quick-start) • [Usage](#-usage) • [Examples](#-examples) • [Configuration](#%EF%B8%8F-configuration)

</div>

---

## 🌟 Features

<table>
<tr>
<td width="50%">

### 🎯 Smart Calendar Management
- 📝 Create events with natural language
- 📅 Fetch today's events instantly
- 🤖 AI-powered event parsing
- ⚡ Lightning-fast responses

</td>
<td width="50%">

### 🔧 Developer Friendly
- 🐍 Pure Python implementation
- 🔐 Secure OAuth 2.0 authentication
- 📦 Easy setup & installation
- 🎨 Clean, modular code

</td>
</tr>
</table>

---

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- Google Cloud Console account
- OpenAI API key

### Installation

```bash
# Clone the repository
git clone https://github.com/paari24/genAI.git
cd genAI/autoGen

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows PowerShell:
.\venv\Scripts\Activate.ps1
# Windows CMD:
.\venv\Scripts\activate.bat
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirement.txt
```

---

## ⚙️ Configuration

### 1. 🔑 Get Google Calendar API Credentials

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing
3. Enable **Google Calendar API**
4. Create **OAuth 2.0 Client ID** (Desktop app)
5. Download credentials as `credentials.json`
6. Place it in the project root directory

### 2. 🌐 Set Authorized Redirect URIs

In Google Cloud Console → OAuth 2.0 Client → Add:
```
http://localhost:8080/
```

### 3. 🔐 Environment Variables

Create a `.env` file in the project root:

```env
OPENAI_API_KEY=your_openai_api_key_here
OPENROUTER_API_KEY=your_openrouter_api_key_here  # Optional
```

---

## 💻 Usage

### Method 1: AI Assistant (Natural Language) 🧠

```python
import asyncio
from get_EventFrom_GmailCalendar import assistant

async def main():
    # Just ask in plain English!
    response = await assistant.run(
        task="Create a team meeting tomorrow at 2 PM for 1 hour"
    )
    print(response.messages[-1].content)

asyncio.run(main())
```

### Method 2: Direct Function Calls 🎯

```python
from datetime import datetime, timedelta
from get_EventFrom_GmailCalendar import create_Event_in_GmailCalendar

# Create event for tomorrow
tomorrow = datetime.now() + timedelta(days=1)
start = tomorrow.replace(hour=14, minute=0, second=0)
end = tomorrow.replace(hour=15, minute=0, second=0)

result = create_Event_in_GmailCalendar(
    summary="Team Standup",
    start_datetime=start.isoformat(),
    end_datetime=end.isoformat(),
    description="Daily sync meeting",
    location="Zoom"
)
print(result)
```

---

## 📋 Examples

### 📅 Fetch Today's Events

```python
from get_EventFrom_GmailCalendar import get_today_Events_from_GmailCalendar

events = get_today_Events_from_GmailCalendar()
print(events)
```

**Output:**
```
📅 Today's Events (2025-10-15):

1. Daily Standup - 09:00 AM @ Zoom
2. Project Review - 02:30 PM @ Conference Room A
3. Team Dinner - 07:00 PM @ Downtown Bistro
```

### ✨ Create Multiple Events

```python
# See create_calendar_event_example.py for full examples
python create_calendar_event_example.py
```

### 🤖 Run AI Assistant

```python
python get_EventFrom_GmailCalendar.py
```

---

## 📁 Project Structure

```
autoGen/
├── 📄 get_EventFrom_GmailCalendar.py    # Main calendar integration
├── 📄 create_calendar_event_example.py  # Usage examples
├── 📄 openRouteraiAssistant.py          # OpenRouter AI client
├── 📄 assistantAgent.py                 # Assistant agent setup
├── 📓 firstAgent.ipynb                  # Jupyter notebook demo
├── 📋 requirement.txt                   # Dependencies
├── 🔐 credentials.json                  # Google OAuth credentials
├── 🎫 token.json                        # Saved auth token (auto-generated)
├── 📝 .env                              # Environment variables
└── 📖 README.md                         # This file
```

---

## 🛠️ Tech Stack

<div align="center">

| Technology | Purpose |
|------------|---------|
| ![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white) | Core Language |
| ![OpenAI](https://img.shields.io/badge/OpenAI-412991?style=for-the-badge&logo=openai&logoColor=white) | AI Model |
| ![Google Calendar](https://img.shields.io/badge/Google_Calendar-4285F4?style=for-the-badge&logo=google-calendar&logoColor=white) | Calendar API |
| ![AutoGen](https://img.shields.io/badge/AutoGen-FF6B6B?style=for-the-badge&logo=robot&logoColor=white) | Agent Framework |

</div>

---

## 🎨 Features in Detail

### 🔥 Natural Language Processing
Ask the AI assistant to manage your calendar using plain English:
- *"Schedule a meeting with John tomorrow at 3 PM"*
- *"What's on my calendar today?"*
- *"Create a lunch appointment for next Monday"*

### 🔐 Secure Authentication
- OAuth 2.0 flow for Google Calendar
- Token persistence (no repeated logins)
- Automatic token refresh

### ⚡ Fast & Efficient
- Asynchronous operations
- Minimal API calls
- Cached authentication

---

## 🐛 Troubleshooting

### Error: `redirect_uri_mismatch`
**Solution:** Add `http://localhost:8080/` to authorized redirect URIs in Google Cloud Console

### Error: `ModuleNotFoundError: No module named 'autogen_agentchat'`
**Solution:** Activate virtual environment and install dependencies:
```bash
.\venv\Scripts\Activate.ps1
pip install -r requirement.txt
```

### Error: `Missing required field 'structured_output'`
**Solution:** This is a warning (not an error). Already fixed in `openRouteraiAssistant.py`

---

## 📊 API Reference

### `create_Event_in_GmailCalendar()`

Creates a new event in Google Calendar.

**Parameters:**
- `summary` (str): Event title *(required)*
- `start_datetime` (str): ISO format start time *(required)*
- `end_datetime` (str): ISO format end time *(required)*
- `description` (str): Event description *(optional)*
- `location` (str): Event location *(optional)*

**Returns:** Confirmation message with event link

---

### `get_today_Events_from_GmailCalendar()`

Fetches all events for the current day.

**Returns:** Formatted string with today's events

---

## 🤝 Contributing

Contributions are welcome! Feel free to:

1. 🍴 Fork the repository
2. 🌿 Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. 💾 Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. 📤 Push to the branch (`git push origin feature/AmazingFeature`)
5. 🎉 Open a Pull Request

---

## 📝 License

This project is open source and available under the [MIT License](LICENSE).

---

## 👨‍💻 Author

**Paari**
- GitHub: [@paari24](https://github.com/paari24)
- Email: paarib24@gmail.com

---

## 🙏 Acknowledgments

- [AutoGen](https://microsoft.github.io/autogen/) - Multi-agent framework
- [Google Calendar API](https://developers.google.com/calendar) - Calendar integration
- [OpenAI](https://openai.com/) - AI models
- [OpenRouter](https://openrouter.ai/) - AI model routing

---

<div align="center">

### ⭐ Star this repo if you find it useful!

Made with ❤️ and 🤖 by [Paari](https://github.com/paari24)

[⬆ Back to Top](#-autogen-google-calendar-assistant)

</div>
