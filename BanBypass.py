import discord
from discord.ext import commands
import time

def read_token(filename="token.txt"):
    with open(filename, "r") as file:
        return file.read().strip()

token = read_token()

bot = commands.Bot(command_prefix="/", intents=discord.Intents.all())
old_servers = {}

@bot.event
async def on_ready():
    global old_servers
    old_servers = {guild.id: (guild.name, None) for guild in bot.guilds}
    print(bot.user.name)

@bot.event
async def on_guild_remove(guild):
    if guild.id in old_servers:
        print(f"Left or removed from server: {old_servers[guild.id][0]}")
        del old_servers[guild.id]
    else:
        print("Left or removed from an unknown server")

@bot.event
async def on_guild_join(guild):
    global old_servers
    try:
        invite = await guild.text_channels[0].create_invite(max_age = 3600)  # Invite valid for 1 hour
        old_servers[guild.id] = (guild.name, invite.url)
    except Exception as e:
        print(f"Could not retrieve/create invite for {guild.name}: {str(e)}")
        old_servers[guild.id] = (guild.name, None)

bot.run(token, bot=False)
