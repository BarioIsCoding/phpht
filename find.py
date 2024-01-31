import discord
import asyncio
import time

client = discord.Client(selfbot=True)

# Read the token from token.txt
with open('token.txt', 'r') as file:
    TOKEN = file.read().strip()

# The specific Group DM ID you want to change
GROUP_DM_ID = 1118868403436916786

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')

    # Find the group DM by ID
    group_dm = client.get_channel(GROUP_DM_ID)
    if group_dm is None or not isinstance(group_dm, discord.GroupChannel):
        print("Group DM not found or bot doesn't have access to it.")
        return

    # Change the group name
    while True:
        try:
            await group_dm.edit(name="Zelensky Supporting Group")
            print("Group name changed successfully.")
        except Exception as e:
            print(f"An error occurred: {e}")
        time.sleep(3)


client.run(TOKEN, bot=False)
