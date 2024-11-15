import requests
import json
from datetime import datetime

# Your bot's API key and chat IDs for the channels
API_KEY = "7545702514:AAG4FIXbWtOsgcoJuZAzPYnLjg0LFDP-asc"

# Chat IDs
DAILY_CHANNEL_ID = "-1002471167965"  # Channel for today's events
ALL_EVENTS_CHANNEL_ID = "-1002467176509"  # Channel for all events

# File paths for the event JSONs
DAILY_EVENTS_JSON = "theloft_today_events.json"
ALL_EVENTS_JSON = "theloft_all_events.json"

def send_message(chat_id, message):
    """Helper function to send a message to a Telegram channel."""
    url = f"https://api.telegram.org/bot{API_KEY}/sendMessage"
    payload = {
        'chat_id': chat_id,
        'text': message,
        'parse_mode': 'Markdown',  # Optional: Makes the message formatted in Markdown
    }
    response = requests.post(url, data=payload)
    return response

def format_event_message(event):
    """Formats event data into a message string."""
    message = (
        f"📅 *Event*: {event['title']}\n"
        f"🗓 *Date*: {event['event_day']}, {event['start_date']}\n"
        f"⏰ *Time*: {event['start_time']} - {event['end_time']}\n"
        f"🎤 *Lineup*: {event['lineup']}\n"
        f"📍 *Location*: {event['location']}\n"
        f"🔗 {event['link']}"
    )
    return message

def send_events_to_channel(json_file, chat_id):
    """Reads the JSON file and sends event messages to the specified Telegram channel."""
    with open(json_file, 'r', encoding='utf-8') as file:
        events = json.load(file)

    for event in events:
        message = format_event_message(event)
        response = send_message(chat_id, message)
        if response.status_code == 200:
            print(f"Successfully sent event: {event['title']}")
        else:
            print(f"Failed to send event: {event['title']}")

# Send today's events to the 'Daily Events' channel
send_events_to_channel(DAILY_EVENTS_JSON, DAILY_CHANNEL_ID)

# Send all events to the 'All Events' channel
send_events_to_channel(ALL_EVENTS_JSON, ALL_EVENTS_CHANNEL_ID)
