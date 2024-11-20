import requests
import json


# Load all events from the JSON file
try:
    with open("b72_all_events.json", "r", encoding="utf-8") as all_file:
        all_events = json.load(all_file)
except FileNotFoundError:
    print("Error: b72_all_events.json file not found.")
    all_events = []

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
