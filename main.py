# bot.py
import os

# import the discord.py module and the commands extension for slash commands
import discord
from discord import app_commands
from discord.ext import commands

# import the dotenv module to load the .env file
from dotenv import load_dotenv

# import custom modules
import handle_quoi as hq

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

# define a command
@tree.command(name="quoi", description="quoi?")
async def feur(ctx):
    await ctx.response.send_message("feur")

# define the prefix for the bot
bot = commands.Bot(command_prefix='!', intents=intents)

#define a global command
@bot.command(name="quoi", description="quoi?")
async def feur(ctx):
    await ctx.send("feur")



# define the function that will be called when the bot is ready
@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')
    await tree.sync()

# run the client
client.run(TOKEN)
