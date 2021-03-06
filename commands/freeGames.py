from discord.ext.commands import Cog, command
from aiohttp import ClientSession
from apscheduler.triggers.cron import CronTrigger


class FreeGames(Cog):
    def __init__(self, bot):
        self.bot = bot
        self.link = 'https://store-site-backend-static.ak.epicgames.com/freeGamesPromotions?locale=ru&country=RU&allowCountries=RU'
        self.bot.scheduler.add_job(
            self.freeGames, CronTrigger(day_of_week='thu', hour=16, minute=3, jitter=120))

    async def freeGames(self, ctx):
        channel = self.bot.get_channel(790625464083152916)
        async with ClientSession() as session:
            async with session.get(self.link) as response:
                resultJson = await response.json()

        games = resultJson['data']['Catalog']['searchStore']['elements']
        for game in games:
            promotions = game['promotions']

            if promotions:
                gameProm = promotions['promotionalOffers']

                if gameProm:
                    game_name = game['title']

                    game_price = game['price']['totalPrice']['fmtPrice']['originalPrice']

                    for attr in game['customAttributes']:
                        if attr['key'] == "com.epicgames.app.productSlug":
                            gameNameInLink = attr['value']

                    link = 'https://www.epicgames.com/store/ru/p/' + gameNameInLink

                    msg = f'Прямо сейчас бесплатна {game_name}\nСтоимость игры {game_price}\nСсылка {link}'

                    await channel.send(msg)


def setup(bot):
    bot.add_cog(FreeGames(bot))
