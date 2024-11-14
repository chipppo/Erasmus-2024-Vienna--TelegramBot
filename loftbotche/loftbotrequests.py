import json
import requests

# Telegram bot credentials
BOT_TOKEN = '7545702514:AAG4FIXbWtOsgcoJuZAzPYnLjg0LFDP-asc'
CHAT_ID = '-1002471167965'

# Load today's events from JSON file
with open("theloft_today_events.json", "r") as f:
    events = json.load(f)

# Send each event as a message
for event in events:
    # Construct message using the provided format
    message = (
        f"📅 *Event*: {event['title']}\n"
        f"🗓 *Date*: {event['event_day']}, {event['start_date']}\n"
        f"⏰ *Time*: {event['start_time']} - {event['end_time']}\n"
        f"🎤 *Lineup*: {event['lineup']}\n"
        f"📍 *Location*: {event['location']}\n"
        f"🔗 {event['link']}"
    )

    # Send the message via Telegram bot
    requests.get(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage", params={
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    })
