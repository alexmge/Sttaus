## @Package: info
# This package contains functions that return embeds for any command that nees to display general information about the bot
#

import discord

## @Function: get_bot_info
# This function returns an embed containing some information about the bot
# @return: An embed containing some information about the bot
def get_bot_info():
    embed = discord.Embed(title="Sttaus", description="Un bot discord très versatile", color=0xeee657)

    # add author
    embed.set_author(name="Alexmge", icon_url="https://avatars.githubusercontent.com/u/82708000?s=400&u=5587bf3b76ae7190fba4b1e0d0b856cb94061e10&v=4")

    #add thumbnail
    embed.set_thumbnail(url="https://i0.wp.com/blog.knoldus.com/wp-content/uploads/2021/05/git-flow.png?fit=275%2C275&ssl=1")

    # add fields
    embed.add_field(name="Version", value="0.1", inline=True)
    embed.add_field(name="Language", value="Python", inline=True)
    embed.add_field(name="Framework", value="discord.py", inline=True)
    embed.add_field(name="Source code", value="https://github.com/alexmge/Sttaus", inline=False)
    embed.add_field(name="Documentation", value="https://alexmge.github.io/Sttaus/", inline=False)
    embed.add_field(name="Development status", value="https://trello.com/b/5aKRG1aS/sttaus-dev-status", inline=False)
    embed.add_field(name="\u200b", value="\u200b", inline=False)

    # add footer
    embed.set_footer(text="\"git sttaus\" Nicolas, 2023")
    return embed

## @Function: get_bot_commands
# This function returns an embed containing the list of commands available
# @return: An embed containing the list of commands available
def get_bot_commands():
    embed = discord.Embed(title="Sttaus", description="Liste des commandes disponibles\n Voir la documentation pour plus de détails : https://alexmge.github.io/Sttaus/", color=0xeee657)
    
    #add thumbnail
    embed.set_thumbnail(url="https://i0.wp.com/blog.knoldus.com/wp-content/uploads/2021/05/git-flow.png?fit=275%2C275&ssl=1")
    embed.add_field(name="\u200b", value="\u200b", inline=False)

    # add fields
    embed.add_field(name="/info", value="Affiche des informations sur le bot", inline=False)
    embed.add_field(name="\u200b", value="\u200b", inline=False)

    embed.add_field(name="/commands", value="Affiche la liste des commandes", inline=False)
    embed.add_field(name="\u200b", value="\u200b", inline=False)

    embed.add_field(name="Agenda", value="", inline=False)
    embed.add_field(name="/add_event", value="Ajoute un événement à l'agenda", inline=True)
    embed.add_field(name="/remove_event", value="Supprime un événement de l'agenda", inline=True)
    embed.add_field(name="/list_events", value="Liste les événements de l'agenda", inline=True)
    embed.add_field(name="\u200b", value="\u200b", inline=False)

    embed.add_field(name="/feature_request", value="Envoie une requête de fonctionnalité au créateur du bot", inline=False)
    embed.add_field(name="\u200b", value="\u200b", inline=False)

    # add footer
    embed.set_footer(text="\"git sttaus\" Nicolas, 2023")
    return embed

## @Function: get_owner_id
# This function returns the id of the bot owner
# @return: The id of the bot owner
def get_owner_id():
    return 581402949524258817