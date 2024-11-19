import requests
import json

# Your bot's API key and the All Events channel ID
API_KEY = ""
ALL_EVENTS_CHANNEL_ID = ""  # Channel for all events
ALL_EVENTS_JSON = "theloft_all_events.json"  # File path for all events JSON

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

def send_events_to_all_channel():
    """Reads all events from the JSON file and sends them to the All Events channel."""
    try:
        with open(ALL_EVENTS_JSON, 'r', encoding='utf-8') as file:
            events = json.load(file)
    except FileNotFoundError:
        print(f"Error: {ALL_EVENTS_JSON} not found.")
        return

    for event in events:
        message = format_event_message(event)
        response = send_message(ALL_EVENTS_CHANNEL_ID, message)
        if response.status_code == 200:
            print(f"Successfully sent event: {event['title']}")
        else:
            print(f"Failed to send event: {event['title']}")

# Send all events
send_events_to_all_channel()
