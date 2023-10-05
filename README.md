# Description
Discord quest but for Aardwolf MUD that idles for quest down and checks for gquests and sends notifications for them

# Setup
Requires you to both setup a message webhook for the Discord channel you're wanting to use as well as registering a bot account for your server. The webhook URL and API key for the bot are both required to for this to work correctly.

# Requires following environmental variables add these to a credential file
AARD_USER - Aardwolf username
AARD_PASS - Aardwolf password
DISCORD_API_KEY - API Key for your chatbot
DISCORD_WEBHOOK - Webhook for same channel

1. docker build -t image-name .
2. docker run --env-file credentials-file image-name

Will add more info as this gets closer to completion