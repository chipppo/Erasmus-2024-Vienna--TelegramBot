import requests
import json
from datetime import datetime

from pyexpat.errors import messages
from telethon.sync import TelegramClient

# Your bot's API key and chat IDs for the channels
API_KEY = ""
DAILY_CHANNEL_ID = ""  # Channel for today's events
ALL_EVENTS_CHANNEL_ID = ""  # Channel for all events
DAILY_EVENTS_JSON = "theloft_today_events.json"
ALL_EVENTS_JSON = "theloft_all_events.json"
SENT_EVENT_URLS_FILE = "sent_event_urls.json"

# Telethon credentials
API_ID = ''  # Obtain from https://my.telegram.org
API_HASH = ''  # Obtain from https://my.telegram.org

# Initialize Telethon client
client = TelegramClient('bot_session', API_ID, API_HASH)


async def delete_last_message(chat_id):
    # Fetch the last message in the channel
    async for message in client.iter_messages(chat_id, limit=1):
        # Delete the last message
        await client.delete_messages(chat_id, message.id)
        print(f"Deleted message with ID: {message.id}")


async def main():
    # Getting information about yourself
    me = await client.get_me()
    print(me.stringify())
    # When you print something, you see a representation of it.
    # You can access all attributes of Telegram objects with
    # the dot operator. For example, to get the username:
    username = me.username
    print(username)
    print(me.phone)
    await delete_last_message(-1002471167965)

with client:
    client.loop.run_until_complete(main())
