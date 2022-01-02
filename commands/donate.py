import discord
from discord import Embed
from discord.ext.commands import Cog, command
from discord.ext.commands.context import Context
from discord_slash import SlashContext, cog_ext

name = "donate"
description = "Пожертвования разработчикам bonzo"
qiwilink = "https://qiwi.com/n/OTTIC882"
telegdonate = "https://t.me/CryptoBot?start=IV8duUiKkI7K"


class Donate(Cog):
    def __init__(self, bot):
        self.bot = bot

    @command(name=name, description=description)
    async def donate_prefix(self, ctx: Context):
        await self.donate(ctx)

    @cog_ext.cog_slash(name=name, description=description)
    async def donate_slash(self, ctx: SlashContext):
        await self.donate(ctx)

    async def donate(self, ctx):
        embed = Embed(
            title="**Способы пожертвований средств разработчикам Bonzo**",
            color=discord.Color.random(),
        )

        embed.set_thumbnail(url="https://i.ibb.co/Xk7qTy4/BOnzo-1.png")

        embed.add_field(
            name="**Для пожертвования через QIWI (RUB):**",
            value=f"**-->** [QIWI/RUB]({qiwilink}) **<--**",
        )
        embed.add_field(
            name="**Для пожертвований с помощью криптовалют:**",
            value=f"**-->** [TELEGRAM/CRYPTO]({telegdonate}) **<--**",
        )

        embed.set_footer(text="/by bonzo/ for THE best! ^-^")

        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Donate(bot))
