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
        embed = Embed(title="**Информация**", color=0x1fcf48)

        embed.set_thumbnail(url="https://i.ibb.co/Xk7qTy4/BOnzo-1.png")

        botLatency = round(ctx.bot.latency * 1000, 2)
        Voice = len(ctx.bot.voice_clients)
        embed.add_field(name="**Status** <a:signal_ping:925751007592480818>", value=f"**ping: **`{botLatency}ms`\n**os: **`{osname}`\n**in voices: **`{Voice}`")

        emojis = len(ctx.bot.emojis)
        guilds = len(ctx.bot.guilds)
        Users  = len(ctx.bot.users)
        embed.add_field(name="**Сounts **<a:slipp:991673495018807376>", value=f"**users: **`{Users} `\n**guilds: **`{guilds} `\n**emojis: **`{emojis}`")
       
        voice_channels_count = 0
        for guild in ctx.bot.guilds:
            voice_channels_count += len(guild.voice_channels)
        channels_count = 0
        for guild in ctx.bot.guilds:
            channels_count += len(guild.channels)
        embed.add_field(name="**Channels count** <a:your_shard:991782924921868418>", value=f"**channels: **`{channels_count}`\n**voices: **`{voice_channels_count}`")


        embed.set_footer(text="/by bonzo/")

        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Status(bot))