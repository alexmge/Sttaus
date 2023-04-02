# bot.py
import os

# import the discord.py module and the commands extension for slash commands
import discord
from discord import app_commands
import asyncio

# import the dotenv module to load the .env file
from dotenv import load_dotenv

# import custom modules
import handle_quoi as hq
import handle_events as he
import info as info

# load the .env file and get the token
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# define the class for the bot
class Sttaus(discord.Client):

    # define the function that will be called when a message is received
    async def on_message(self, message):
        # if the message contains any occurrence of "quoi"
        if "quoi" in message.content:
            # call the function
            await hq.respond_feur(message)
        print(f'Message from {message.author}: {message.content}')

# create the client
intents = discord.Intents.default()
intents.message_content = True
client = Sttaus(intents=intents)

# create the command tree for slash commands
tree = app_commands.CommandTree(client=client)

scheduler = he.Scheduler(client)

################################################################
######################## Slash commands ########################
################################################################

# Command that returns some infos about the bot
@tree.command(name="info", description="Display some infos about the bot")
async def feur(ctx):
    infos = info.get_bot_info()
    await ctx.response.send_message(embed=infos)

# Command that adds an event to the scheduler
@tree.command(name="add_event", description="Add an event to the scheduler")
async def add(ctx, name: str, date: str, time: str):
    # Check for arguments validity
    if not name or not date or not time:
        await ctx.response.send_message("Usage: /add <name> <date> <time>")
        return
    if not date.isnumeric() or not time.isnumeric():
        await ctx.response.send_message("Date and time must be numbers")
        return
    if len(date) != 8 or len(time) != 4:
        await ctx.response.send_message("Date must be in the format DDMMYYYY and time must be in the format HHMM")
        return
    # Add the event to the scheduler
    await scheduler.add_event(ctx, name, date, time)

# Command that removes an event from the scheduler
@tree.command(name="remove_event", description="Remove an event from the scheduler")
async def remove(ctx, name: str):
    # Check for arguments validity
    if not name:
        await ctx.response.send_message("Usage: /remove <name>")
        return
    # Remove the event from the scheduler
    await scheduler.remove_event(ctx, name)

# Command that lists the events in the scheduler in an embed
@tree.command(name="list_events", description="List the events in the scheduler")
async def list(ctx):
    await scheduler.list_events(ctx)

################################################################
################################################################

# define the function that will be called when the bot is ready
@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')
    await tree.sync()

# run the client
client.run(TOKEN)
