import discord
from discord.ext import commands

# Variables for the strings
trigger_string = "{ping}"
replacement_string = "@​​​ВetterMint"

# Read the bot token from the file
with open('token.txt', 'r') as token_file:
    bot_token = token_file.read().strip()

bot = commands.Bot(command_prefix='/', selfbot=True)

@bot.event
async def on_message(message):
    # Check if the message contains the trigger string
    if trigger_string in message.content:
        # Delete the original message
        await message.delete()

        # Replace the trigger string with the replacement string
        new_content = message.content.replace(trigger_string, replacement_string)

        # Find the last message of the user "bettermint"
        async for msg in message.channel.history(limit=500):
            if msg.author.name == "bettermint":
                # Reply to the found message
                await msg.reply(new_content)
                break

    # Process commands
    await bot.process_commands(message)

# Start the bot with the token from the file
bot.run(bot_token, bot=False)
