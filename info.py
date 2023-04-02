import discord

def get_bot_info():
    embed = discord.Embed(title="Sttaus", description="Un bot discord très versatile", color=0xeee657)

    # add author
    embed.set_author(name="Alexmge", icon_url="https://avatars.githubusercontent.com/u/82708000?s=400&u=5587bf3b76ae7190fba4b1e0d0b856cb94061e10&v=4")

    #add thumbnail
    embed.set_thumbnail(url="https://i0.wp.com/blog.knoldus.com/wp-content/uploads/2021/05/git-flow.png?fit=275%2C275&ssl=1")

    # Add title field
    embed.add_field(name="Feur", value="Réponds feur dès que quelqu'un dit quoi", inline=True)

    # add empty field
    embed.add_field(name="\u200b", value="\u200b", inline=False)

    # add footer
    embed.set_footer(text="\"git sttaus\" Nicolas, 2023")
    return embed
