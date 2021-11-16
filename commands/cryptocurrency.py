from discord.embeds import Embed
from commands.resources.AutomatedMessages import automata
from discord.ext.commands import Cog, command, CommandError, Context
from aiohttp import ClientSession
from discord_slash import SlashContext, cog_ext
from discord_slash.error import SlashCommandError
from datetime import datetime
from os import getenv

name = 'crypto'
description = 'Выводит информацию о криптовалюте (INDEV)'


class RequestNetworkError(CommandError, SlashCommandError):
    pass


class CurrencyDoesNotExist(CommandError, SlashCommandError):
    pass


class Dvach(Cog):
    LISTINGS_URL = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest"

    def __init__(self, bot):
        self.bot = bot
        self.key = getenv('COINMARKETCAP_API_KEY')

        self.HEADERS = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Accept-Encoding': 'deflate, gzip',
            "X-CMC_PRO_API_KEY": str(self.key)
        }

    async def cog_command_error(self, ctx, error):
        if isinstance(error, RequestNetworkError):
            return await ctx.send(embed=automata.generateEmbErr('Ошибка при запросе'))
        if isinstance(error, CurrencyDoesNotExist):
            return await ctx.send(embed=automata.generateEmbErr('Такой валюты не найдено'))

    @Cog.listener()
    async def on_slash_command_error(self, ctx, error):
        if isinstance(error, RequestNetworkError):
            return await ctx.send(embed=automata.generateEmbErr('Ошибка при запросе'))
        if isinstance(error, CurrencyDoesNotExist):
            return await ctx.send(embed=automata.generateEmbErr('Такой валюты не найдено'))

    # @command(name=name, description=description)
    # async def get_crypto_info_prefix(self, ctx: Context, currency: str):
    #     await self.get_crypto_info(ctx, currency)

    # @cog_ext.cog_slash(name=name, description=description)
    # async def get_crypto_info_slash(self, ctx: SlashContext, currency: str):
    #     await self.get_crypto_info(ctx, currency)

    # async def get_crypto_info(self, ctx, currency):
    #     async with ClientSession(headers=self.HEADERS) as session:
    #         async with session.get(self.URL, params=self.PARAMS) as response:
    #             res = await response.json()
    #             if res.status == 404:
    #                 raise CurrencyDoesNotExist

    #     await ctx.send(res)

    @command(name='crypto_listings', description='Показывает топ 10 криптовалют по капитализации')
    async def get_crypto_listings_prefix(self, ctx: Context):
        await self.get_crypto_listings(ctx)

    @cog_ext.cog_slash(name='crypto_listings', description='Показывает топ 10 криптовалют по капитализации')
    async def get_crypto_listings_slash(self, ctx: SlashContext):
        await self.get_crypto_listings(ctx)

    async def get_crypto_listings(self, ctx):
        params = {
            "start": "1",
            "limit": "10",
            "convert": "USD"
        }
        async with ClientSession(headers=self.HEADERS) as session:
            async with session.get(self.LISTINGS_URL, params=params) as response:
                res = (await response.json())['data']
        embed = Embed(title='10 крупнейших криптовалют по капитализации')

        embed.set_footer(text=f'Обновлено в ' +
                         datetime.fromisoformat(res[0]['last_updated'][:-1]).strftime('%Hh %Mm %Ss - %d %h %Y UTC'))

        for crypto in res:
            finprice = float(crypto['quote']['USD']['price'])
            if finprice > 99.9:
                finprice=str(int(round(finprice, 1)))
            elif finprice > 0.0099:
                finprice=str(round(finprice, 2))
            else:
                finprice = str(round(finprice, 6))
            
            embed.add_field(
                name=f"{crypto['name']} | {crypto['symbol']}", value=f"Цена: ${finprice}")
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Dvach(bot))
