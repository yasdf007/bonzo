from discord.embeds import Embed
from commands.resources.AutomatedMessages import automata
from discord.ext.commands import Cog, command, CommandError, Context, hybrid_command
from aiohttp import ClientSession
from datetime import datetime
from os import getenv

name = "crypto"
description = "Выводит информацию о криптовалюте (INDEV)"


class RequestNetworkError(CommandError):
    pass


class CurrencyDoesNotExist(CommandError):
    pass


class Crypto(Cog):
    LISTINGS_URL = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest"

    def __init__(self, bot):
        self.bot = bot
        self.key = getenv("COINMARKETCAP_API_KEY")

        self.HEADERS = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Accept-Encoding": "deflate, gzip",
            "X-CMC_PRO_API_KEY": str(self.key),
        }

    async def cog_command_error(self, ctx, error):
        if isinstance(error, RequestNetworkError):
            return await ctx.send(embed=automata.generateEmbErr("Ошибка при запросе"))
        if isinstance(error, CurrencyDoesNotExist):
            return await ctx.send(
                embed=automata.generateEmbErr("Такой валюты не найдено")
            )
        raise error
        
    @hybrid_command(name=name, description=description)
    async def get_crypto_listings(self, ctx):
        params = {"start": "1", "limit": "10", "convert": "USD"}
        async with ClientSession(headers=self.HEADERS) as session:
            async with session.get(self.LISTINGS_URL, params=params) as response:
                res = (await response.json())["data"]
        embed = Embed(title="10 крупнейших криптовалют по капитализации")

        embed.set_footer(
            text=f"Обновлено в "
            + datetime.fromisoformat(res[0]["last_updated"][:-1]).strftime(
                "%Hh %Mm %Ss - %d %h %Y UTC"
            )
        )

        for crypto in res:
            finprice = float(crypto["quote"]["USD"]["price"])
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
    await bot.add_cog(Crypto(bot))
