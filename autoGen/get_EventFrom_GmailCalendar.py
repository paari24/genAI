from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient
from dotenv import load_dotenv
import os
import asyncio
from datetime import datetime, timedelta
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import json

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

# Initialize OpenAI model client
model_client = OpenAIChatCompletionClient(
    api_key=api_key,
    model="gpt-4o-mini"
)

# Google Calendar API scopes
SCOPES = ['https://www.googleapis.com/auth/calendar']

def get_calendar_service():
    """
    Authenticate and return the Google Calendar service.
    """
    creds = None
    # Check if token.json exists (stores user's access and refresh tokens)
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    
    # If there are no valid credentials, let the user log in
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            # Use port 8080 explicitly - make sure to add http://localhost:8080/ to authorized redirect URIs in Google Cloud Console
            creds = flow.run_local_server(port=8080, prompt='consent', access_type='offline')
        
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    
    service = build('calendar', 'v3', credentials=creds)
    return service

# --- Google Calendar Tool Methods ---
def create_Event_in_GmailCalendar(summary: str, start_datetime: str, end_datetime: str, description: str = "", location: str = "") -> str:
    """
    Create an event in the user's Google Calendar.
    Args:
        summary (str): Event title/summary
        start_datetime (str): Start datetime in ISO format (e.g., "2025-10-15T10:00:00")
        end_datetime (str): End datetime in ISO format (e.g., "2025-10-15T11:00:00")
        description (str): Event description (optional)
        location (str): Event location (optional)
    Returns:
        str: Confirmation message with event details
    """
    try:
        service = get_calendar_service()
        
        event = {
            'summary': summary,
            'location': location,
            'description': description,
            'start': {
                'dateTime': start_datetime,
                'timeZone': 'Asia/Kolkata',  # Adjust timezone as needed
            },
            'end': {
                'dateTime': end_datetime,
                'timeZone': 'Asia/Kolkata',
            },
            'reminders': {
                'useDefault': True,
            },
        }
        
        event_result = service.events().insert(calendarId='primary', body=event).execute()
        return f"✅ Event created successfully!\nTitle: {summary}\nStart: {start_datetime}\nEnd: {end_datetime}\nEvent Link: {event_result.get('htmlLink')}"
    
    except Exception as e:
        return f"❌ Error creating event: {str(e)}"

def get_today_Events_from_GmailCalendar() -> str:
    """
    Fetch today's events from the user's Google Calendar.
    Returns:
        str: Formatted list of today's events
    """
    try:
        service = get_calendar_service()
        
        # Get today's date range
        now = datetime.now()
        start_of_day = datetime(now.year, now.month, now.day, 0, 0, 0).isoformat() + 'Z'
        end_of_day = datetime(now.year, now.month, now.day, 23, 59, 59).isoformat() + 'Z'
        
        # Call the Calendar API
        events_result = service.events().list(
            calendarId='primary',
            timeMin=start_of_day,
            timeMax=end_of_day,
            singleEvents=True,
            orderBy='startTime'
        ).execute()
        
        events = events_result.get('items', [])
        
        if not events:
            return "📅 No events found for today."
        
        # Format events
        event_list = [f"📅 Today's Events ({now.strftime('%Y-%m-%d')}):\n"]
        for idx, event in enumerate(events, 1):
            start = event['start'].get('dateTime', event['start'].get('date'))
            summary = event.get('summary', 'No title')
            location = event.get('location', '')
            
            # Parse and format time
            if 'T' in start:
                start_time = datetime.fromisoformat(start.replace('Z', '+00:00'))
                time_str = start_time.strftime('%I:%M %p')
            else:
                time_str = 'All day'
            
            event_info = f"{idx}. {summary} - {time_str}"
            if location:
                event_info += f" @ {location}"
            event_list.append(event_info)
        
        return "\n".join(event_list)
    
    except Exception as e:
        return f"❌ Error fetching events: {str(e)}"

assistant = AssistantAgent(
    name="my_Assistant",
    model_client=model_client,
    description="Event organizer Assistant",
    system_message="You are a helpful assistant that helps users to manage their events in Google Calendar. You can create events and fetch today's events from the user's Google Calendar. Use the tools below to interact with Google Calendar.",
    tools={get_today_Events_from_GmailCalendar, create_Event_in_GmailCalendar}
)

async def manage_calendar_events():
    # Example 1: Get today's events
    print("=" * 60)
    print("FETCHING TODAY'S EVENTS")
    print("=" * 60)
    response = await assistant.run(task="Get today's events from my calendar")
    print(response.messages[-1].content)
    
    # Example 2: Create a new event
    print("\n" + "=" * 60)
    print("CREATING A NEW EVENT")
    print("=" * 60)
    response = await assistant.run(
        task="Create an event titled 'Team Meeting' for tomorrow at 2:00 PM to 3:00 PM with description 'Discuss project updates'"
    )
    print(response.messages[-1].content)

asyncio.run(manage_calendar_events())