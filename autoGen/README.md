<div align="center">

# 🤖✨ AutoGen AI Agent Framework

<img src="https://img.shields.io/badge/Python-3.8+-blue.svg" alt="Python Version">
<img src="https://img.shields.io/badge/AutoGen-Latest-green.svg" alt="AutoGen">
<img src="https://img.shields.io/badge/Google_Calendar-API-red.svg" alt="Google Calendar">
<img src="https://img.shields.io/badge/OpenAI-GPT--4-purple.svg" alt="OpenAI">
<img src="https://img.shields.io/badge/Multi--Modal-Supported-orange.svg" alt="Multi-Modal">

### *Comprehensive AI Agent Framework with Calendar Integration, Tools, and Multi-Modal Support* �

[Features](#-features) • [Quick Start](#-quick-start) • [Examples](#-examples) • [Project Files](#-project-files) • [Configuration](#%EF%B8%8F-configuration)

</div>

---

## 🌟 Features

<table>
<tr>
<td width="50%">

### 🎯 Smart AI Agents
- 🤖 Multiple agent types and configurations
- 📝 Natural language understanding
- 🔧 Custom tool integration
- 📊 Event observation and streaming
- 🎨 Multi-modal support (text + images)

</td>
<td width="50%">

### 📅 Calendar Management
- ✅ Create events with natural language
- � Fetch today's events instantly
- 🔐 Secure OAuth 2.0 authentication
- ⚡ Lightning-fast responses
- 🌍 Timezone support

</td>
</tr>
<tr>
<td width="50%">

### �️ Developer Tools
- 🐍 Pure Python implementation
- � Modular architecture
- 🎯 Easy-to-use APIs
- 📖 Comprehensive examples
- 🔄 Async/await support

</td>
<td width="50%">

### 🌐 AI Model Support
- � OpenAI GPT models
- 🔀 OpenRouter integration
- � Multiple model clients
- 🚀 Streaming responses
- 💬 Message handling

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

### 🤖 Basic Assistant

```python
# assistantAgent.py
from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient

model_client = OpenAIChatCompletionClient(api_key=api_key, model="gpt-4o-mini")
assistant = AssistantAgent(name="my_Assistant", model_client=model_client)

response = await assistant.run(task="How are you?")
print(response.messages[-1].content)
```

### 🛠️ Agent with Tools

```python
# toolsAgentai.py
def get_weather(city: str) -> str:
    return f"The weather in {city} is sunny with 25°C."

assistant = AssistantAgent(
    name="my_Assistant",
    model_client=model_client,
    tools={get_weather}  # Add custom tools
)

response = await assistant.run(task="Get weather for Chennai")
```

### 📊 Observing Agent Events

```python
# running_ObservingAgent.py
response = await assistant.on_messages(
    messages=[TextMessage(role="user", content="Get weather", source="user")],
    cancellation_token=CancellationToken()
)

print("Inner Messages:", response.inner_messages)
print("Chat Message:", response.chat_message)
```

### 🌊 Streaming Responses

```python
# streamingmessage.py
async for message in assistant.on_messages_stream(
    messages=[TextMessage(content="Tell me a story", source="user")]
):
    print(message, end="", flush=True)
```

### 🖼️ Multi-Modal (Text + Images)

```python
# image_multimodel_Autogen.py
from autogen_agentchat.messages import MultiModalMessage

message = MultiModalMessage(
    content=["What's in this image?", Image(image_url)],
    source="user"
)
response = await assistant.run(task=message)
```

### 📅 Calendar Events

```python
# get_EventFrom_GmailCalendar.py
# Fetch today's events
events = get_today_Events_from_GmailCalendar()
print(events)

# Create an event
from datetime import datetime, timedelta

tomorrow = datetime.now() + timedelta(days=1)
start = tomorrow.replace(hour=14, minute=0)
end = tomorrow.replace(hour=15, minute=0)

result = create_Event_in_GmailCalendar(
    summary="Team Meeting",
    start_datetime=start.isoformat(),
    end_datetime=end.isoformat(),
    description="Quarterly review",
    location="Conference Room A"
)
```

---

## 📁 Project Structure

```
autoGen/
├── 📄 assistantAgent.py                      # Basic assistant agent setup
├── 📄 openRouteraiAssistant.py               # OpenRouter AI client configuration
├── 📄 agentCustomization_PromptEngineering.py # Custom prompt engineering examples
├── 📄 toolsAgentai.py                        # Agent with tool integration
├── 📄 messages_in_Autogen.py                 # Message handling examples
├── 📄 running_ObservingAgent.py              # Event observation and monitoring
├── 📄 streamingmessage.py                    # Streaming response handling
├── 📄 image_multimodel_Autogen.py            # Multi-modal (text + image) support
├── 📄 get_EventFrom_GmailCalendar.py         # Google Calendar integration
├── 📄 create_calendar_event_example.py       # Calendar usage examples
├── 📓 firstAgent.ipynb                       # Jupyter notebook demo
├── 📋 requirement.txt                        # Project dependencies
├── 🔐 credentials.json                       # Google OAuth credentials
├── 🎫 token.json                             # Saved auth token (auto-generated)
├── 📝 .env                                   # Environment variables
└── 📖 README.md                              # This file
```

---

## 📚 Project Files Explained

### 🔧 Core Agent Files

#### `assistantAgent.py`
Basic assistant agent implementation with OpenAI integration.

```python
python assistantAgent.py
```

#### `openRouteraiAssistant.py`
Alternative AI client using OpenRouter for model flexibility.

```python
python openRouteraiAssistant.py
```

#### `agentCustomization_PromptEngineering.py`
Examples of customizing agents with prompt engineering techniques.

```python
python agentCustomization_PromptEngineering.py
```

### 🛠️ Advanced Features

#### `toolsAgentai.py`
Demonstrates how to equip agents with custom tools (e.g., weather lookup).

```python
python toolsAgentai.py
```

#### `messages_in_Autogen.py`
Shows how to work with different message types (TextMessage, MultiModalMessage).

```python
python messages_in_Autogen.py
```

#### `running_ObservingAgent.py`
Monitor agent execution with event observation and inner message inspection.

```python
python running_ObservingAgent.py
```

**Key Features:**
- View `ToolCallRequestEvent` - when agent calls a tool
- View `ToolCallExecutionEvent` - tool execution results
- Access `inner_messages` and `chat_message`

#### `streamingmessage.py`
Real-time streaming responses from AI agents.

```python
python streamingmessage.py
```

#### `image_multimodel_Autogen.py`
Multi-modal AI agent that can process both text and images.

```python
python image_multimodel_Autogen.py
```

### 📅 Calendar Integration

#### `get_EventFrom_GmailCalendar.py`
Full Google Calendar integration with AI assistant.

**Features:**
- Create events with natural language
- Fetch today's events
- OAuth 2.0 authentication

```python
python get_EventFrom_GmailCalendar.py
```

#### `create_calendar_event_example.py`
Standalone examples for creating calendar events programmatically.

```python
python create_calendar_event_example.py
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
