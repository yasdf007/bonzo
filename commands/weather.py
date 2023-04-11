from discord import Embed
from discord.ext.commands import Cog, hybrid_command, Context
from dependencies.api.weather.abc import WeatherAPI
from bot import Bot
from typing import List
from discord.app_commands import Choice, autocomplete
from discord import Interaction
from .resources.exceptions import CustomCheckError

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
        self.openweather_api: WeatherAPI = self.bot.dependency.openweather_api
        self.wttr_api: WeatherAPI = self.bot.dependency.wttr_api

 
    @hybrid_command(name=name, description=description)
    @autocomplete(provider=provider_autocomplete)
    async def getWeather(self, ctx: Context, city: str, provider: str = 'openweather'):
        if provider == 'openweather':
            res = await self.openweather_api.get_weather_data(city)
        elif provider == 'wttr':
            res = await self.wttr_api.get_weather_data(city)
        else:
            raise CustomCheckError(message='Неправильный провайдер погоды')
        if not res:
            raise CustomCheckError(message='Запрашиваемый город не найден')


        embed = Embed(
            title=f'Погода: {res.city}:', color=0x543964)

        embed.add_field(name='На улице:', value=res.weatherType, inline=False)
        embed.add_field(name='Температура :thermometer:',
                        value=f'{res.temp} °C', inline=False)
        embed.add_field(name='Скорость ветра :dash:',
                        value=f'{res.wind_direction} {res.wind_speed} м/с', inline=False)
        embed.add_field(name='Влажность:droplet:',
                        value=f'{res.humidity} %', inline=False)
        embed.set_footer(text='Powered by openweathermap.org')

        await ctx.send(embed=embed)



async def setup(bot):
    await bot.add_cog(weather(bot))
