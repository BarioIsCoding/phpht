import discord
import asyncio

def read_token(filename="token.txt"):
    with open(filename, "r") as file:
        return file.read().strip()

bot = discord.bot()

# Dictionary to store the content of the last sticky message for each channel
stickies = {}
# Dictionary to store the ID of the last non-sticky message for each channel
last_messages = {}

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

@bot.event
async def on_message(message):

    # Check if the message is a command to set a sticky
    if message.content.startswith('/ssticky'):
            if message.author != bot.user:
                content = message.content[len('/ssticky '):].strip()
                await set_sticky(message.channel, content)

    # Repost the sticky if the last message wasn't the sticky
    elif message.channel.id in stickies:
        if message.author != bot.user:
            if last_messages.get(message.channel.id) != message.id:
                await repost_sticky(message.channel)

async def set_sticky(channel, content):
    """Sets or updates the sticky message for a channel."""
    sticky_message = await channel.send(content)
    stickies[channel.id] = content
    last_messages[channel.id] = sticky_message.id

async def repost_sticky(channel):
    """Reposts the sticky message."""
    new_sticky = await channel.send(stickies[channel.id])
    last_messages[channel.id] = new_sticky.id

token = read_token()
bot.run(token, bot=False)
