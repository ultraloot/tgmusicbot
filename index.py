import requests
import json

# Replace YOUR_BOT_TOKEN with your actual bot token
bot_token = '5419432479:AAHzAriBK9gszQlIXsFF9ifOzgfDQ8W9DTk'

# Replace YOUR_CHANNEL_USERNAME with your channel username
channel_username = 'UltimateTools_Deals'

# API URL for Telegram bot requests
api_url = f'https://api.telegram.org/bot{bot_token}/'

# Get updates from Telegram API
def get_updates():
    response = requests.get(api_url + 'getUpdates')
    return response.json().get('result', [])

# Check if the user has joined the channel
def has_joined_channel(user_id):
    url = api_url + f'getChatMember?chat_id=@{channel_username}&user_id={user_id}'
    response = requests.get(url)
    return response.json()['ok'] and response.json()['result']['status'] == 'member'

# Handle messages
def handle_message(message):
    chat_id = message['chat']['id']
    message_text = message['text']

    if message_text == '/start':
        # Send a welcome message
        response = 'Welcome to the bot! To get your user ID, please send /id command.'
        requests.get(api_url + f'sendMessage?chat_id={chat_id}&text={response}')
    elif message_text == '/id':
        # Check if the user has joined the channel
        user_id = message['from']['id']
        if has_joined_channel(user_id):
            # Send the user ID
            response = f'Your user ID is {user_id}'
            requests.get(api_url + f'sendMessage?chat_id={chat_id}&text={response}')
        else:
            # Prompt the user to join the channel
            response = f'Please join the channel @{channel_username} to get your user ID.'
            requests.get(api_url + f'sendMessage?chat_id={chat_id}&text={response}')

# Start the bot
def start_bot():
    last_update_id = None
    while True:
        updates = get_updates()
        if updates:
            for update in updates:
                if last_update_id is None or update['update_id'] > last_update_id:
                    last_update_id = update['update_id']
                    if 'message' in update:
                        handle_message(update['message'])

# Run the bot
if __name__ == '__main__':
    start_bot()
