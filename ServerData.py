import discord
import tkinter as tk
from tkinter import ttk
import threading
import asyncio
from PIL import Image, ImageTk
import requests
from io import BytesIO
from datetime import datetime, timedelta

# Read the bot token from the file
with open('token.txt', 'r') as file:
    TOKEN = file.read().strip()

# Initialize the Discord client
intents = discord.Intents.default()
intents.guilds = True
intents.members = True
intents.emojis = True
intents.messages = True
intents.guild_messages = True
client = discord.Client(intents=intents,selfbot=True)

# Global variable to store guilds
guilds = []



# Function to fetch guild information
async def fetch_guild_info(guild):
    # Count number of bots in the guild
    bot_count = sum(1 for member in guild.members if member.bot)

    # Fetch all roles with colors
    roles = [(role.name, f'#{role.color.value:06x}' if role.color.value != 0 else '#000000') for role in guild.roles]

    # Fetch emojis
    emojis = [emoji for emoji in guild.emojis]

    icon_url = str(guild.icon_url)
    response = requests.get(icon_url)
    icon_image = Image.open(BytesIO(response.content))
    icon_image = icon_image.resize((100, 100), Image.ANTIALIAS)  # Resize the icon
    icon_photo = ImageTk.PhotoImage(icon_image)

    # Count messages in the last 24 hours (this might not be accurate and can be resource-intensive)
    message_count = 0
    current_time = datetime.utcnow()
    for channel in guild.text_channels:
        try:
            async for message in channel.history(limit=None, after=current_time - timedelta(hours=1)):
                message_count += 1
        except discord.errors.Forbidden:
            pass  # Skip channels where the bot doesn't have permission

    try:
        invites = await guild.invites()
        main_invite = invites[0].url if invites else "No invite found"
    except:
        main_invite = "No permission to create/view invites"


    owner = await guild.fetch_member(guild.owner_id)  # Fetch the owner

    return {
        'name': guild.name,
        'id': guild.id,
        'primary_language': str(guild.preferred_locale),
        'channel_count': len(guild.channels),
        'bot_count': bot_count,
        'role_count': len(guild.roles),
        'roles': roles,
        'emojis': emojis,
        'icon_photo': icon_photo,
        'main_invite': main_invite,
        'member_count': guild.member_count,
        'region': str(guild.region),
        'created_at': guild.created_at.strftime("%Y-%m-%d %H:%M:%S"),
        'owner': str(owner),
        'is_community': 'Yes' if guild.features and "COMMUNITY" in guild.features else 'No',
        'message_count_1h': message_count,
    }

# Function to handle guild selection
def on_guild_selected(event):
    selected_index = guild_dropdown.current()
    if selected_index >= 0:  # Check if a valid guild is selected
        selected_guild = guilds[selected_index]
        asyncio.run_coroutine_threadsafe(fetch_guild_info(selected_guild), client.loop).add_done_callback(lambda future: update_guild_info(future.result()))

# Function to update the GUI with guild information
def update_guild_info(guild_info):
    text_widget.config(state=tk.NORMAL)
    text_widget.delete(1.0, tk.END)

    # Display basic info
    basic_info = {k: v for k, v in guild_info.items() if k not in ['roles', 'emojis', 'icon_photo']}
    info_text = '\n'.join([f'{key}: {value}' for key, value in basic_info.items()])
    text_widget.insert(tk.END, info_text + '\n\n')

    # Display roles with colors
    text_widget.insert(tk.END, 'Roles:\n')
    for role, color in guild_info['roles']:
        tag_name = role.replace(" ", "_")
        text_widget.tag_configure(tag_name, foreground=color)
        text_widget.insert(tk.END, role + '\n', tag_name)

    # Display emojis
    text_widget.insert(tk.END, '\nEmojis:\n')
    for emoji in guild_info['emojis']:
        text_widget.insert(tk.END, str(emoji) + ' ')

    # Display server icon
    icon_label.config(image=guild_info['icon_photo'])
    icon_label.image = guild_info['icon_photo']  # Keep a reference

    text_widget.config(state=tk.DISABLED)


    #Initialize the GUI
root = tk.Tk()
root.title("Discord Bot Guild Info")

# Create a dropdown for guilds
guild_var = tk.StringVar(root)
guild_dropdown = ttk.Combobox(root, textvariable=guild_var)
guild_dropdown.bind('<<ComboboxSelected>>', on_guild_selected)

# Create a text widget for displaying guild information
text_widget = tk.Text(root, state=tk.DISABLED, wrap=tk.WORD)
text_widget.pack(expand=True, fill=tk.BOTH)

# Create a label for the server icon
icon_label = tk.Label(root)
icon_label.pack()

# Function to update the dropdown with guilds
def update_guild_dropdown():
    global guilds
    guilds = client.guilds
    guild_dropdown['values'] = [guild.name for guild in guilds]
    guild_dropdown.pack()

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')
    root.after(0, update_guild_dropdown)

# Run the Discord client in a separate thread
def run_discord_bot():
    client.run(TOKEN, bot=False)

bot_thread = threading.Thread(target=run_discord_bot)
bot_thread.start()

# Start the tkinter GUI event loop
root.mainloop()
