import requests
import json

# Telegram bot token and chat ID
BOT_TOKEN = "7958779435:AAHkYL-e0anpkU-SktSENyAj1bCjRnB5yB0"
CHAT_ID = "-1002471167965"

# Load events from the JSON file
with open("viper_room_events_today.json", "r", encoding="utf-8") as f:
    events = json.load(f)

# Send a message for each event in today's JSON file
for event in events:
    title = event["title"]
    link = event["link"]
    location = event["location"]

    # Create message content
    message = (
        f"📅 *Event*: {title}\n"
        f"🗓 *Date*: {event['date']}\n"
        f"📍 *Location*: {location}\n"
        f"🔗 [View Event]({link})"
    )

    # Send the message via Telegram API
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    }
    response = requests.post(url, json=payload)

    # Check for successful send
    if response.status_code == 200:
        print(f"Message sent for event: {title}")
    else:
        print(f"Failed to send message for event: {title}, status code: {response.status_code}")
