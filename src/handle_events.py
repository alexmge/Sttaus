## @package handle_events
# This module contains the functions that handle the events.
# The events are stored in the events.json file, which is a JSON file.
# The file is structured like this:
# {
#     "events": [
#         {
#             "name": "event name",
#             "date": "event date",
#             "time": "event time"
#         },
#         {
#             "name": "event name",
#             "date": "event date",
#             "time": "event time"
#         }
#     ]
# }

# The scheduler is used to remind people of upcoming events deadlines.
# It looks for events in the events.json file and sends a message :
# - 3 days before the event -> "@epita L'événement "<event name>" se termine dans 3 jours"
# - 1 day before the event -> "@epita L'événement "<event name>" se termine dans 1 jour"
# - 2 hour before the event -> "@epita L'événement "<event name>" se termine dans 2 heures"
# - when the event is passed -> "L'événement "<event name>" est passé"
#
# The scheduler is called every 30 seconds to check for events.
#
# The way it knows when to send a message is by
# checking the field "next_reminder" in the events.json file.
# The field is updated every time a message is sent. After the last reminder is sent,
# the "next_reminder" field is set to "None", and the event will be deleted from the file
# after the due date is passed.

import json
import os
import datetime
import discord
from discord.ext import tasks, commands

# get the path of the current file
path = os.path.dirname(os.path.abspath(__file__))
# path to events.json
events_path = path + "/events.json"

## The Scheduler class is, as its name suggests, a scheduler.
# It manages the events and sends reminders to the calendar channel.
# It is called every 30 seconds.
class Scheduler():
    
    def __init__(self, client):
        self.client = client
        self.CALENDAR_CHANNEL_ID = os.getenv('CALENDAR_CHANNEL')

    @tasks.loop(seconds=30)
    async def scheduler(self):
        # Check if the events.json file exists and throw an error if it doesn't
        if not os.path.exists(events_path):
            raise FileNotFoundError("The events.json file does not exist")
        # Open the file and load the events
        with open(events_path, "r") as f:
            events = json.load(f)
        # Get the current date and time
        now = datetime.datetime.now()
        # Loop through the events
        for event in events["events"]:
            # Check if the event is in the past
            if datetime.datetime.strptime(event["date"] + event["time"], "%d%m%Y%H%M") < now:
                # Delete the event
                events["events"].remove(event)
                # Send a message to the channel
                await self.client.get_channel(int(self.CALENDAR_CHANNEL_ID)).send("L'événement " + event["name"] + " est passé")
            # Check the next reminder
            elif event["next_reminder"] != None:
                # Get the date and time of the next reminder
                next_reminder = datetime.datetime.strptime(event["next_reminder"], "%d%m%Y%H%M")
                # Check if the next reminder is due
                if next_reminder <= now:
                    # Send a message to the channel
                    await self.client.get_channel(int(self.CALENDAR_CHANNEL_ID)).send("L'événement " + event["name"] + " se termine dans " + compute_time_difference(event["date"], event["time"]))
                    # Update the next reminder
                    event["next_reminder"] = compute_next_reminder(event["date"], event["time"])

        # Save the events
        with open(events_path, "w") as f:
            json.dump(events, f, indent=4, separators=(',', ': '))

    async def add_event(self, ctx, name: str, date: str, time: str):
        # Add the event to the scheduler
        # Check if the events.json file exists
        if not os.path.exists(events_path):
            # Create the file
            with open(events_path, "w") as f:
                json.dump({"events": []}, f)
        # Open the file and load the events
        with open(events_path, "r") as f:
            events = json.load(f)
        # Add the event to the list if name not already present
        for event in events["events"]:
            if event["name"] == name:
                await ctx.response.send_message("L'événement " + name + " existe déjà")
                return
            
        # compute the next reminder
        next_reminder = compute_next_reminder(date, time)

        # if the event is too close or passed, don't add it
        if next_reminder == None:
            await ctx.response.send_message("L'événement " + name + " est trop proche ou alors déjà passé")
            return
        
        events["events"].append({"name": name, "date": date, "time": time, "next_reminder": next_reminder})
        # Save the events
        with open(events_path, "w") as f:
            json.dump(events, f, indent=4, separators=(',', ': '))
        await ctx.response.send_message("L'événement " + name + " a été ajouté au scheduler")
    
    async def remove_event(self, ctx, name: str):
        # Remove an event from the scheduler
        # Check if the events.json file exists
        if not os.path.exists(events_path):
            await ctx.response.send_message("Aucun événement n'est enregistré")
            return
        # Open the file and load the events
        with open(events_path, "r") as f:
            events = json.load(f)
        # Remove the event from the list
        for event in events["events"]:
            if event["name"] == name:
                events["events"].remove(event)
                # Save the events
                with open(events_path, "w") as f:
                    json.dump(events, f, indent=4, separators=(',', ': '))
                await ctx.response.send_message("L'événement " + name + " a été supprimé du scheduler")
                return
        await ctx.response.send_message("L'événement " + name + " n'existe pas")
    
    # List the events and send them to the channel in an embed
    async def list_events(self, ctx):
        # Check if the events.json file exists
        if not os.path.exists(events_path):
            await ctx.response.send_message("Aucun événement n'est enregistré")
            return
        # Open the file and load the events
        with open(events_path, "r") as f:
            events = json.load(f)
        # Create the embed
        embed = discord.Embed(title="Liste des événements", description="Voici la liste des événements enregistrés : ", color=0x00ff00)
        for event in events["events"]:
            # format the date and time
            date = datetime.datetime.strptime(event["date"], "%d%m%Y")
            time = datetime.datetime.strptime(event["time"], "%H%M")
            # Add the event to the embed
            embed.add_field(name=event["name"],value= "Se termine le " + date.strftime("%d/%m/%Y") + " à " + time.strftime("%H:%M"), inline=False)
        await ctx.response.send_message(embed=embed)

def compute_next_reminder(date, time):
    # if the event is in more than 3 days, return 3 days
    if datetime.datetime.strptime(date + time, "%d%m%Y%H%M") > datetime.datetime.now() + datetime.timedelta(days=3):
        return (datetime.datetime.strptime(date + time, "%d%m%Y%H%M") - datetime.timedelta(days=3)).strftime("%d%m%Y%H%M")
    # if the event is in more than 1 day, return 1 day
    if datetime.datetime.strptime(date + time, "%d%m%Y%H%M") > datetime.datetime.now() + datetime.timedelta(days=1):
        return (datetime.datetime.strptime(date + time, "%d%m%Y%H%M") - datetime.timedelta(days=1)).strftime("%d%m%Y%H%M")
    # if the event is in more than 2 hours, return 2 hours
    if datetime.datetime.strptime(date + time, "%d%m%Y%H%M") > datetime.datetime.now() + datetime.timedelta(hours=2):
        return (datetime.datetime.strptime(date + time, "%d%m%Y%H%M") - datetime.timedelta(hours=2)).strftime("%d%m%Y%H%M")
    # if the event is less than 2 hours or passed, return None
    return None
    
# returns the time difference in weeks, days and hours between now and the date and time given in parameters
# if weeks > 0, days and hours are not returned
# if days > 0, hours is not returned
def compute_time_difference(date, time):
    # Get the date and time of the event
    event_date = datetime.datetime.strptime(date, "%d%m%Y")
    event_time = datetime.datetime.strptime(time, "%H%M")
    # concatenate the date and time
    event_date = datetime.datetime.combine(event_date, event_time.time())
    # Get the difference between now and the event
    difference = event_date - datetime.datetime.now()
    # add 1 minute
    difference += datetime.timedelta(minutes=1)
    # Compute the number of weeks, days and hours
    weeks = difference.days // 7
    days = difference.days % 7
    hours = difference.seconds // 3600
    minutes = (difference.seconds % 3600) // 60
    # Return the time difference
    if weeks > 0:
        return str(weeks) + " semaines"
    elif days > 0:
        return str(days) + " jours"
    else: 
        return str(hours) + " heures " + str(minutes) + " minutes"
