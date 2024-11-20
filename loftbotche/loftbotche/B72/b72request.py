import requests
import json
from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetHistoryRequest
from telethon.tl.functions.messages import DeleteMessagesRequest


# JSON file paths
DAILY_EVENTS_JSON = "b72_events_today.json"
ALL_EVENTS_JSON = "b72_all_events.json"

# Initialize Telethon client
client = TelegramClient('bot_session', API_ID, API_HASH)

# Function to send messages to Telegram using the bot API
def send_message_via_bot(chat_id, message):
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
        print(f"Failed to send message to chat ID {chat_id}. Status code: {response.status_code}")

# Function to load events from JSON
def load_events(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Error: {file_path} file not found.")
        return []

# Function to retrieve all messages from a channel
async def fetch_channel_messages(chat_id):
    messages = []
    async for message in client.iter_messages(chat_id):
        if message.text:
            messages.append(message)
    return messages

# Function to compare event URLs with existing messages
def get_existing_urls(messages):
    urls = set()
    for message in messages:
        if "http" in message.text:  # Look for URLs in message text
            lines = message.text.split("\n")
            for line in lines:
                if line.startswith("🔗 [View Event]("):
                    start = line.find("(") + 1
                    end = line.find(")")
                    if start != -1 and end != -1:
                        urls.add(line[start:end])
    return urls

# Main logic
async def post_events_and_remove_duplicates():
    # Load events from JSON
    today_events = load_events(DAILY_EVENTS_JSON)
    all_events = load_events(ALL_EVENTS_JSON)

    # Fetch existing messages from both channels
    existing_messages_today = await fetch_channel_messages(CHAT_ID_TODAY)
    existing_messages_all = await fetch_channel_messages(CHAT_ID_ALL)

    # Get existing URLs from messages in both channels
    existing_urls_today = get_existing_urls(existing_messages_today)
    existing_urls_all = get_existing_urls(existing_messages_all)

    # 1. Delete old duplicate messages from the 'Today' channel
    for message in existing_messages_today:
        if "http" in message.text:
            lines = message.text.split("\n")
            for line in lines:
                if line.startswith("🔗 [View Event]("):
                    start = line.find("(") + 1
                    end = line.find(")")
                    if start != -1 and end != -1:
                        url = line[start:end]
                        if url in existing_urls_today:
                            await client.delete_messages(CHAT_ID_TODAY, message.id)
                            print(f"Deleted duplicate message in TODAY channel: {message.id}")

    # 2. Delete old duplicate messages from the 'All' channel
    for message in existing_messages_all:
        if "http" in message.text:
            lines = message.text.split("\n")
            for line in lines:
                if line.startswith("🔗 [View Event]("):
                    start = line.find("(") + 1
                    end = line.find(")")
                    if start != -1 and end != -1:
                        url = line[start:end]
                        if url in existing_urls_all:
                            await client.delete_messages(CHAT_ID_ALL, message.id)
                            print(f"Deleted duplicate message in ALL channel: {message.id}")

    # 3. Reset the URL sets to ensure new events are posted (even if the URLs were previously deleted)
    existing_urls_today.clear()
    existing_urls_all.clear()

    # 4. Send today's events after deletion
    for event in today_events:
        if event["link"] not in existing_urls_today:
            message = (
                f"📅 *Event*: {event['title']}\n"
                f"🗓 *Date*: {event['date']}\n"
                f"📍 *Location*: {event['location']}\n"
                f"🔗 [View Event]({event['link']})"
            )
            send_message_via_bot(CHAT_ID_TODAY, message)
            existing_urls_today.add(event["link"])  # Add to existing URLs to prevent re-sending

    # 5. Send all events after deletion
    for event in all_events:
        if event["link"] not in existing_urls_all:
            message = (
                f"📅 *Event*: {event['title']}\n"
                f"🗓 *Date*: {event['date']}\n"
                f"📍 *Location*: {event['location']}\n"
                f"🔗 [View Event]({event['link']})"
            )
            send_message_via_bot(CHAT_ID_ALL, message)
            existing_urls_all.add(event["link"])  # Add to existing URLs to prevent re-sending


# Run the script
with client:
    client.loop.run_until_complete(post_events_and_remove_duplicates())
