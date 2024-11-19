import requests
import json

# Your bot's API key and the Daily Events channel ID
API_KEY = "7545702514:AAG4FIXbWtOsgcoJuZAzPYnLjg0LFDP-asc"
DAILY_CHANNEL_ID = "-1002471167965"  # Channel for today's events
DAILY_EVENTS_JSON = "theloft_today_events.json"  # File path for today's events JSON

def send_message(chat_id, message):
    """Helper function to send a message to a Telegram channel."""
    url = f"https://api.telegram.org/bot{API_KEY}/sendMessage"
    payload = {
        'chat_id': chat_id,
        'text': message,
        'parse_mode': 'Markdown',
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

def send_events_to_daily_channel():
    """Reads today's events from the JSON file and sends them to the Daily Events channel."""
    try:
        with open(DAILY_EVENTS_JSON, 'r', encoding='utf-8') as file:
            events = json.load(file)
    except FileNotFoundError:
        print(f"Error: {DAILY_EVENTS_JSON} not found.")
        return

    for event in events:
        message = format_event_message(event)
        response = send_message(DAILY_CHANNEL_ID, message)
        if response.status_code == 200:
            print(f"Successfully sent event: {event['title']}")
        else:
            print(f"Failed to send event: {event['title']}")

# Send today's events
send_events_to_daily_channel()
