import requests
import time
from datetime import datetime



# Function to send messages to Telegram
def send_message(chat_id, message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": message,
        "parse_mode": "Markdown",
    }
    response = requests.post(url, json=payload)

    if response.status_code == 200:
        print(f"Message sent to chat ID {chat_id}: {message}")
    else:
        print(
            f"Failed to send message to chat ID {chat_id}. Status code: {response.status_code}, Response: {response.text}")


# Function to filter and validate events
def get_valid_events(events):
    today = datetime.now()
    valid_events = []

    for event in events:
        event_date = datetime.strptime(event["date"], "%d.%m.%Y")
        if event_date >= today:
            valid_events.append(event)

    return valid_events


# Mock list of events (replace with actual scraping logic)
events = [
    {"title": "Band A Live", "date": "24.12.2024", "location": "Viper Room, LA", "link": "https://example.com/event1"},
    {"title": "Band B Performance", "date": "26.12.2024", "location": "Viper Room, LA",
     "link": "https://example.com/event2"},
    {"title": "Band C Night", "date": "30.12.2024", "location": "Viper Room, LA", "link": "https://example.com/event3"},
]

# Filter valid events
valid_events = get_valid_events(events)

# Send messages for valid events with a delay
if valid_events:
    for event in valid_events:
        title = event["title"]
        date = event["date"]
        location = event["location"]
        link = event["link"]

        message = (
            f"📅 *Event*: {title}\n"
            f"🗓 *Date*: {date}\n"
            f"📍 *Location*: {location}\n"
            f"🔗 [View Event]({link})"
        )

        send_message(CHAT_ID_ALL, message)

        # Add a delay to avoid hitting rate limits
        time.sleep(1)  # Adjust the delay as needed
else:
    send_message(CHAT_ID_ALL, "No valid events found at Viper Room.")
