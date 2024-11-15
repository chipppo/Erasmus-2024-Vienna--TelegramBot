import requests
import json

# Telegram bot token
BOT_TOKEN = "7672829764:AAEuNRPH_geZc1b4HG2tckQdncczKl2S9RE"

# Chat IDs
CHAT_ID_TODAY = "-1002471167965"  # Channel for today's events
CHAT_ID_ALL = "-1002278732286"  # Channel for all events

# Load events from JSON files
with open("b72_events_today.json", "r", encoding="utf-8") as today_file:
    today_events = json.load(today_file)

with open("b72_all_events.json", "r", encoding="utf-8") as all_file:
    all_events = json.load(all_file)

# Function to send messages to Telegram
def send_message(chat_id, message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": message,
        "parse_mode": "Markdown"
    }
    response = requests.post(url, json=payload)

    # Log message sending status
    if response.status_code == 200:
        print(f"Message sent to chat ID {chat_id}: {message}")
    else:
        print(f"Failed to send message to chat ID {chat_id}. Status code: {response.status_code}")

# Format and send today's events
if today_events:
    for event in today_events:
        title = event["title"]
        date = event["date"]
        link = event["link"]
        location = event["location"]

        message = (
            f"📅 *Event*: {title}\n"
            f"🗓 *Date*: {date}\n"
            f"📍 *Location*: {location}\n"
            f"🔗 [View Event]({link})"
        )
        send_message(CHAT_ID_TODAY, message)
else:
    send_message(CHAT_ID_TODAY, "No events are happening today at B72.")

# Format and send all events
if all_events:
    for event in all_events:
        title = event["title"]
        date = event["date"]
        link = event["link"]
        location = event["location"]

        message = (
            f"📅 *Event*: {title}\n"
            f"🗓 *Date*: {date}\n"
            f"📍 *Location*: {location}\n"
            f"🔗 [View Event]({link})"
        )
        send_message(CHAT_ID_ALL, message)
else:
    send_message(CHAT_ID_ALL, "No events are currently listed at B72.")
