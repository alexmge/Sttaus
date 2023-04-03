## @package slash_commands
# This module contains the SlashCommands class, which is used to manage the slash commands of the bot

from discord import app_commands
import info

class SlashCommands():
    def __init__(self, scheduler, client):
        self.tree = app_commands.CommandTree(client=client)
        self.scheduler = scheduler
        self.client = client
    
    def init_slash_commands(self):
        ## /info command
        # Command that displays some infos about the bot
        @self.tree.command(name="info", description="Display some infos about the bot")
        async def help(ctx):
            infos = info.get_bot_info()
            await ctx.response.send_message(embed=infos)

        ## /commands command
        # Command that displays the list of commands
        @self.tree.command(name="commands", description="Display the list of commands")
        async def commands(ctx):
            commands = info.get_bot_commands()
            await ctx.response.send_message(embed=commands)

        ## /add_event command
        # Command that adds an event to the scheduler
        # @param name The name of the event
        # @param date The date of the event in the format DDMMYYYY
        # @param time The time of the event in the format HHMM
        @self.tree.command(name="add_event", description="Add an event to the scheduler")
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
            await self.scheduler.add_event(ctx, name, date, time)

        ## /remove_event command
        # Command that removes an event from the scheduler
        # @param name The name of the event
        @self.tree.command(name="remove_event", description="Remove an event from the scheduler")
        async def remove(ctx, name: str):
            # Check for arguments validity
            if not name:
                await ctx.response.send_message("Usage: /remove <name>")
                return
            # Remove the event from the scheduler
            await self.scheduler.remove_event(ctx, name)

        ## /list_events command
        # Command that lists the events in the scheduler along with their date and time
        @self.tree.command(name="list_events", description="List the events in the scheduler")
        async def list(ctx):
            await self.scheduler.list_events(ctx)
        
        ## /feature_request command
        # Command that sends a feature request to the bot owner
        # @param request The feature request
        @self.tree.command(name="feature_request", description="Send a feature request to the bot owner")
        async def feature_request(ctx, request: str):
            # Check for arguments validity
            if not request:
                await ctx.response.send_message("Usage: /feature_request <request>")
                return
            # Send the feature request to the bot owner
            await self.client.get_user(info.get_owner_id()).send(f"Feature request from {ctx.author.name}#{ctx.author.discriminator}: {request}")
            await ctx.response.send_message("Your feature request has been sent to the bot owner")
