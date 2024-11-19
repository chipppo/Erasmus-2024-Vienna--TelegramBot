import requests
import json

# Telegram bot token
BOT_TOKEN = "7958779435:AAHkYL-e0anpkU-SktSENyAj1bCjRnB5yB0"

# Chat ID for today's events
CHAT_ID_TODAY = "-1002471167965"  # Channel for today's events

# Load today's events from the JSON file
try:
    with open("viperroom_events_today.json", "r", encoding="utf-8") as today_file:
        today_events = json.load(today_file)
except FileNotFoundError:
    print("Error: viperroom_events_today.json file not found.")
    today_events = []

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
    send_message(CHAT_ID_TODAY, "No events are happening today at Viper Room.")
