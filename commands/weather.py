from discord import Embed, Emoji
from discord.ext import commands
import os
from dotenv import load_dotenv
import requests
import json
load_dotenv()


class weather(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Хендл ошибок
    async def cog_command_error(self, ctx, error):
        if isinstance(error, commands.CommandInvokeError):
            await ctx.send(error.original)

    @commands.command(aliases=['weather', 'погода'])
    async def getWeatherInfo(self, ctx, city):
        weatherToken = os.getenv('WEATHER_TOKEN')
        query = f'https://api.openweathermap.org/data/2.5/weather?q={city}&lang=ru&units=metric&appid={weatherToken}'
        result = requests.get(query)

        if(result.status_code == 404):
            raise commands.CommandInvokeError('Город не найден')

        jsonResult = json.loads(result.text)

        weatherCountry = jsonResult['sys']['country'].lower()
        weatherType = jsonResult['weather'][0]['description']
        weatherTemp = str(round(jsonResult['main']['temp'])) + "°C"
        weatherTempMin = str(round(jsonResult['main']['temp_min'])) + "°C"
        weatherTempMax = str(round(jsonResult['main']['temp_max'])) + "°C"
        weatherWind = jsonResult['wind']['speed']

        embed = Embed(
            title=f'Погода: {city} :flag_{weatherCountry}:', color=0x543964)
        embed.add_field(name='Погода', value=weatherType, inline=False)
        embed.add_field(name='Температура', value=weatherTemp, inline=False)
        embed.add_field(name='Максимальная температура',
                        value=weatherTempMax, inline=False)
        embed.add_field(name='Минимальная температура',
                        value=weatherTempMin, inline=False)
        embed.add_field(name='Скорость ветра',
                        value=f'{weatherWind} м/c', inline=False)
        embed.set_footer(text='Powered by openweathermap.org')

        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(weather(bot))
