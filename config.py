import os

credentials = {
    'username': os.environ.get('AARD_USER'),
    'password': os.environ.get('AARD_PASS'),
    'discord_api_key': os.environ.get('DISCORD_API_KEY'),
    'discord_webhook': os.environ.get('DISCORD_WEBHOOK'),
}