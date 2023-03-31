from discord import Embed
from discord.ext.commands.context import Context
from discord.ext.commands import Cog, command, CommandError, MissingRequiredArgument, hybrid_command
from os import getenv
from dotenv import load_dotenv
from aiohttp import ClientSession
from .resources.AutomatedMessages import automata
from dependencies.api.weather.abc import WeatherAPI, Response 

name = 'weather'
description = 'Погода по запрашиваемому городу'


class CityNotFound(CommandError):
    pass

class BlankCityName(CommandError):
    pass

class InvalidProvider(CommandError):
    pass

class weather(Cog):
    def __init__(self, bot):
        self.bot = bot
        self.openweather_api: WeatherAPI = self.bot.dependency.openweather_api
        self.wttr_api: WeatherAPI = self.bot.dependency.wttr_api

    async def cog_command_error(self, ctx, error):
        if isinstance(error, MissingRequiredArgument):
            return await ctx.send(embed=automata.generateEmbErr('Город не указан', error=error))
        if isinstance(error, InvalidProvider):
            return await ctx.send(embed=automata.generateEmbErr('Неправильный провайдер погоды', error=error))
        if isinstance(error, CityNotFound):
            return await ctx.send(embed=automata.generateEmbErr('Запрашиваемый город не найден', error=error))
        if isinstance(error, (BlankCityName, MissingRequiredArgument)):
            return await ctx.send(embed=automata.generateEmbErr('Город не указан', error=error))
        raise error

 
    @hybrid_command(name=name, description=description)
    async def getWeather(self, ctx, city, provider='openweather'):
        if provider == 'openweather':
            res = await self.openweather_api.get_response(city)
        elif provider == 'wttr':
            res = await self.wttr_api.get_response(city)
        else:
            raise InvalidProvider()
        if not res:
            raise CityNotFound()

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
