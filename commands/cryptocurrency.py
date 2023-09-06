from discord.embeds import Embed
from discord.ext.commands import Cog, Context, hybrid_command
from bot import Bot

from dependencies.api import coinmarketcap

from config import COINMARKETCAP_API_KEY

name = "crypto"
description = "Выводит информацию о криптовалюте (INDEV)"

class Crypto(Cog):
    def __init__(self, bot, cmc: coinmarketcap.CoinmarketcapAPI):
        self.bot: Bot = bot
        self.cmc = cmc

    @hybrid_command(name=name, description=description)
    async def get_crypto_listings(self, ctx: Context):
        res = await self.cmc.get_biggest_currencies()

        embed = Embed(title="10 крупнейших криптовалют по капитализации")

        for crypto in res:
            finprice = float(crypto['price_usd'])
            if finprice > 99.9:
                finprice = str(int(round(finprice, 1)))
            elif finprice > 0.0099:
                finprice = str(round(finprice, 2))
            else:
                finprice = str(round(finprice, 6))

            embed.add_field(
                name=f"{crypto['name']} | {crypto['symbol']}",
                value=f"Цена: ${finprice}",
            )
        await ctx.send(embed=embed)


async def setup(bot):
    cmc = coinmarketcap.CoinmarketcapAPI(COINMARKETCAP_API_KEY)
    await bot.add_cog(Crypto(bot, cmc))
