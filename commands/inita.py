import discord
from discord import Embed
from discord.ext.commands import Cog, command, hybrid_command
from discord.ext.commands.context import Context

name = "init"
description = "Краткая информация об использовании бота / How to start?"
supportserver = "https://discord.gg/kjUdcUGw"


class Inita(Cog):
    def __init__(self, bot):
        self.bot = bot


    @hybrid_command(name=name, description=description)
    async def inita(self, ctx):
        embed = Embed(title="**Начало работы с bonzo**", color=discord.Color.random())

        if ctx.guild.id in self.bot.custom_prefix:
            prefix = self.bot.custom_prefix[ctx.guild.id]
        else:
            prefix = "b/"

        embed.set_thumbnail(url="https://i.ibb.co/Xk7qTy4/BOnzo-1.png")

        embed.add_field(
            name="**Для использования legacy-команд:**", value=f"{prefix}help"
        )
        embed.add_field(name="**Для использования slash-команд:**", value="/help_slash")
        embed.add_field(
            name="**Для изменения префикса:**", value="@Bonzo set_prefix [ваш префикс]"
        )
        embed.add_field(
            name="**Для связи с разработчиками:**",
            value=f"[Перейдите на сервер (нажмите сюда)]({supportserver})",
        )

        embed.set_footer(text="/by bonzo/ for everyone :)")

        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Inita(bot))
