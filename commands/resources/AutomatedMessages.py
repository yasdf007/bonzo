import discord
import datetime

from discord import Embed
from discord import Colour

class automata:

    def generateEmbErr(x: str, error=None):
        result = Embed(
            title=f'**{x}**', color=Colour.red()
        )
        if error:
            readableErr = type(error).__name__
            result.set_footer(text=f'Error message / by Bonzo / {readableErr}')
        else:
            result.set_footer(text='Error message / by Bonzo /')
        return result

    # def generateEmbInfo(x: str):
    #     result = Embed(
    #         title=f'**{x}**',
    #         color=randCol()
    #     )
    #     result.set_footer(text='')
    #     return result


Embeds = {
    "error": {
        "title": "**Error**",
        "colour": discord.Colour.red(),
    },
    "warn": {
        "title": "**Warning**",
        "colour": discord.Colour.yellow(),
    },
    "success": {
        "title": "**Success**",
        "colour": discord.Colour.green(),
    },
    "info": {
        "title": "**Info**",
        "colour": discord.Colour.blurple(),
    },  
}



class AutoEmbed():
    def __init__(self, author_name=None, author_url=None, author_icon=None):

        self.author_name = author_name
        self.author_url  = author_url
        self.author_icon = author_icon

    def autoembed(
       self,
       title: str,
       description: str,
       color = discord.Colour.blurple(),
       thumbnail: str = None,
       image: str = None,
       timestamp = datetime.datetime.now()
    ):

        
        embed = discord.Embed(
            title=title,
            description=description,
            colour=color,
            timestamp=timestamp
        )

        if self.author_url and self.author_name and self.author_icon:
            embed.set_author(
                name     = self.author_name,
                icon_url = self.author_icon,
                url      = self.author_url
            )

        if thumbnail:
            embed.set_thumbnail(thumbnail)

        if image:
            embed.set_image(url=image)

        return embed

    def type_autoembed(
        self,
        type: str,
        description: str,
        timestamp = datetime.datetime.now()
    ):
        
        
        embed = discord.Embed(
        title=Embeds[type]["title"],
        description=description,
        colour=Embeds[type]["colour"],
        timestamp=timestamp
        )

        return embed
