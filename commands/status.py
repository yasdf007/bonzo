import os
import discord
from discord import Embed
from discord.ext.commands import Cog, command, CommandError
from discord.ext.commands.context import Context
from discord_slash import SlashContext, cog_ext
from .resources.AutomatedMessages import automata
from discord_slash.error import SlashCommandError
from discord.ext.commands import Bot
from config import guilds

name = "status"
description = "Статус бота на данный момент"
osname = os.name

class Status(Cog):
    def __init__(self, bot):
        self.bot = bot

    @command(name=name, description=description)
    async def status_prefix(self, ctx: Context):
        await self.status(ctx)   


    @cog_ext.cog_slash(name=name, description=description)
    async def status_slash(self, ctx: SlashContext):
        await self.status(ctx)

        #статус бота

    async def status(self, ctx):
        embed = Embed(title="**Статус** 🔘", color=0x1fcf48)

        embed.set_thumbnail(url="https://i.ibb.co/Xk7qTy4/BOnzo-1.png")
		
        botLatency = round(ctx.bot.latency * 1000, 2)
        embed.add_field(name="**Ping:**", value=f"`{botLatency}ms `🟢")
        embed.add_field(
            name="**OS:**", value=f"`{osname} `🟢"
        )

        Voice = len(ctx.bot.voice_clients)
        embed.add_field(
            name="**In voices:**", value=f"`{Voice} `🟢"
        )

        Users = len(ctx.bot.users)
        embed.add_field(
            name="**Users count:**", value=f"`{Users} `ℹ️"
        )

        guilds = len(ctx.bot.guilds)
        embed.add_field(
            name="**Guilds count:**", value=f"`{guilds} `ℹ️"
        )

        emojis = len(ctx.bot.emojis)
        embed.add_field(
            name="**Emojis count:**", value=f"`{emojis} `ℹ️"
        )

        channels_count = 0
        for guild in ctx.bot.guilds:
            channels_count += len(guild.channels)
        embed.add_field(
            name="**Channels count:**", value=f"`{channels_count} `ℹ️"
        )

        voice_channels_count = 0
        for guild in ctx.bot.guilds:
            voice_channels_count += len(guild.voice_channels)
        embed.add_field(
            name="**Voices count:**", value=f"`{voice_channels_count} `ℹ️"
        )

        embed.set_footer(text="/by bonzo/ altNodes")

        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Status(bot))