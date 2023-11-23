from discord import Embed, app_commands, Interaction
from discord.ext.commands import Cog
from bot import Bot
from typing import List
from discord.app_commands import Choice, autocomplete
from discord import Interaction
from .resources.exceptions import CustomCheckError
from .resources.weather.weather import get_provider

name = 'weather'
description = 'Погода по запрашиваемому городу'



async def provider_autocomplete(
    interaction: Interaction,
    current: str,
) -> List[Choice[str]]:
    providers = ['openweather',  'wttr']
    return [
        Choice(name=provider, value=provider)
        for provider in providers if current.lower() in provider.lower()
    ]


class weather(Cog):
    def __init__(self, bot):
        self.bot: Bot = bot
 
    @app_commands.command(name=name, description=description)
    @autocomplete(provider=provider_autocomplete)
    async def getWeather(self, inter: Interaction, city: str, provider: str = 'openweather'):
        weather_provider = get_provider(provider)

        res = await weather_provider.get_weather_data(city)
        if not res:
            raise CustomCheckError(message='Запрашиваемый город не найден')

        embed = Embed(
            title=f'Погода: {res["city"]}:', color=0x543964)

        embed.add_field(name='На улице:', value=res['weatherType'], inline=False)
        embed.add_field(name='Температура :thermometer:',
                        value=f'{res["temp"]} °C', inline=False)
        embed.add_field(name='Скорость ветра :dash:',
                        value=f'{res["wind_direction"]} {res["wind_speed"]} м/с', inline=False)
        embed.add_field(name='Влажность:droplet:',
                        value=f'{res["humidity"]} %', inline=False)

        await inter.response.send_message(embed=embed)



async def setup(bot):
    await bot.add_cog(weather(bot))
