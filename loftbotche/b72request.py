import requests
import json
from datetime import datetime

# Telegram bot token and chat ID
BOT_TOKEN = "7672829764:AAEuNRPH_geZc1b4HG2tckQdncczKl2S9RE"
CHAT_ID = "-1002471167965"

# Load events from the JSON file
with open("b72_events_today.json", "r", encoding="utf-8") as f:
    events = json.load(f)

# Get today's date in the format YYYY-MM-DD
today = datetime.now().strftime("%Y-%m-%d")

# Send a message for each event happening today
for event in events:
    if event["date"] == today:
        title = event["title"]
        link = event["link"]

        # Create message content
        message = (
            f"📅 *Event*: {title}\n"
            f"🗓 *Date*: {event['date']}\n"
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
