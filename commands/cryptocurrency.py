from discord import app_commands, Interaction
from discord.embeds import Embed
from discord.ext.commands import Cog
from bot import Bot

from dependencies.api import coinmarketcap

from config import COINMARKETCAP_API_KEY

def format_price_usdt(price: float):
    if price > 99.9:
        return round(price, 1)
    elif price > 0.0099:
        return round(price, 2)
    else:
       return round(price, 6)

class Crypto(Cog):
    def __init__(self, bot, cmc: coinmarketcap.CoinmarketcapAPI):
        self.bot: Bot = bot
        self.cmc = cmc

    @app_commands.command(name="crypto", description= "Выводит информацию о криптовалюте (INDEV)")
    async def get_crypto_listings(self, inter: Interaction):
        res = await self.cmc.get_biggest_currencies()

        embed = Embed(title="10 крупнейших криптовалют по капитализации")

        for crypto in res:
            price = format_price_usdt( float(crypto['price_usd']))
            embed.add_field(
                name=f"{crypto['name']} | {crypto['symbol']}",
                value=f"Цена: ${price}",
            )

        await inter.response.send_message(embed=embed)


async def setup(bot):
    cmc = coinmarketcap.CoinmarketcapAPI(COINMARKETCAP_API_KEY)
    await bot.add_cog(Crypto(bot, cmc))
