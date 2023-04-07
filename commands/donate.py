import discord
from discord import Embed
from discord.ext.commands import Cog, hybrid_command, Context
from bot import Bot

name = "donate"
description = "Пожертвования разработчикам bonzo"
qiwilink = "https://qiwi.com/n/OTTIC882"
telegdonate = "https://t.me/CryptoBot?start=IV8duUiKkI7K"


class Donate(Cog):
    def __init__(self, bot):
        self.bot: Bot = bot


    @hybrid_command(name=name, description=description)
    async def donate(self, ctx: Context):
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


async def setup(bot):
    await bot.add_cog(Donate(bot))
