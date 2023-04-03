import os
# import the discord.py module and the commands extension for slash commands
import discord
from discord import app_commands
# import the dotenv module to load the .env file
from dotenv import load_dotenv
# import custom modules
import handle_quoi as hq
import handle_events as he
import slash_commands as sc

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
intents.members = True
intents.guilds = True
client = Sttaus(intents=intents)

# create the scheduler
scheduler = he.Scheduler(client=client)

# create the slash commands tree
cog = sc.SlashCommands(scheduler=scheduler, client=client)
cog.init_slash_commands()

# define the function that will be called when the bot is ready
@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')
    await cog.tree.sync()
    await scheduler.scheduler.start()

# run the client
client.run(TOKEN)
