import discord

# Initialize the Discord client
class MyClient(discord.Client):
    # Event listener for when the bot has switched from offline to online.
    async def on_ready(self):
        print('Logged in as', self.user)

    # Event listener for when a new message is sent to a channel.
    async def on_message(self, message):
        # Don't respond to messages sent by the bot itself
        if message.author == self.user:
            return

        # Check if the message contains "nuh uh"
        if "yuh uh" in message.content.lower():
            # Send "yuh uh" in response
            await message.channel.send("nuh uh")

# Create a bot instance with your specific configurations
client = MyClient(selfbot=True)

# Reading the bot token from token.txt
with open('token.txt', 'r') as file:
    token = file.read().strip()

client.run(token, bot=False)