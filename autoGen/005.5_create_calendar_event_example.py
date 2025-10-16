"""
Examples of how to create Google Calendar events
"""
from get_EventFrom_GmailCalendar import create_Event_in_GmailCalendar, get_today_Events_from_GmailCalendar
from datetime import datetime, timedelta

# Example 1: Create a simple event for tomorrow
print("=" * 60)
print("Example 1: Simple event for tomorrow")
print("=" * 60)

tomorrow = datetime.now() + timedelta(days=1)
start_time = tomorrow.replace(hour=10, minute=0, second=0, microsecond=0)
end_time = tomorrow.replace(hour=11, minute=0, second=0, microsecond=0)

result = create_Event_in_GmailCalendar(
    summary="Coffee Meeting",
    start_datetime=start_time.isoformat(),
    end_datetime=end_time.isoformat(),
    description="Catch up with the team",
    location="Starbucks Downtown"
)
print(result)

# Example 2: Create an event for today
print("\n" + "=" * 60)
print("Example 2: Event for today afternoon")
print("=" * 60)

today = datetime.now()
start_time = today.replace(hour=14, minute=30, second=0, microsecond=0)
end_time = today.replace(hour=15, minute=30, second=0, microsecond=0)

result = create_Event_in_GmailCalendar(
    summary="Project Review",
    start_datetime=start_time.isoformat(),
    end_datetime=end_time.isoformat(),
    description="Review Q4 project deliverables",
    location="Conference Room A"
)
print(result)

# Example 3: Create an all-day event (1-hour placeholder)
print("\n" + "=" * 60)
print("Example 3: Quick 30-min standup")
print("=" * 60)

next_week = datetime.now() + timedelta(days=7)
start_time = next_week.replace(hour=9, minute=0, second=0, microsecond=0)
end_time = next_week.replace(hour=9, minute=30, second=0, microsecond=0)

result = create_Event_in_GmailCalendar(
    summary="Daily Standup",
    start_datetime=start_time.isoformat(),
    end_datetime=end_time.isoformat(),
    description="Daily team sync"
)
print(result)

# Example 4: Show all today's events after creating
print("\n" + "=" * 60)
print("Current Events for Today")
print("=" * 60)
result = get_today_Events_from_GmailCalendar()
print(result)
