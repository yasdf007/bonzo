from commands.resources.animationFW import reColoring
from discord import Embed, Color
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

    @commands.command(name='weather', description='Погода по запрашиваемому городу', aliases=['погода'])
    async def getWeather(self, ctx, *args):
        city = ' '.join(args)

        weatherToken = os.getenv('WEATHER_TOKEN')
        query = f'https://api.openweathermap.org/data/2.5/weather?q={city}&lang=ru&units=metric&appid={weatherToken}'
        result = requests.get(query)

        if(result.status_code == 404):
            raise commands.CommandInvokeError(f'Город {city} не найден')

        jsonResult = json.loads(result.text)

        weatherCountry = jsonResult['sys']['country'].lower()
        weatherType = jsonResult['weather'][0]['description']
        weatherTemp = round(jsonResult['main']['temp'])
        weatherWindSpeed = jsonResult['wind']['speed']
        weatherHumidity = jsonResult['main']['humidity']
        weatherDirection = await self.convertWindDirection((jsonResult['wind']['deg']))

        if jsonResult['dt'] > jsonResult['sys']['sunrise'] and jsonResult['dt'] < jsonResult['sys']['sunset']:
            weatherIsDay = True
        else:
            weatherIsDay = False

        weatherId = await self.getWeatherMoji(str((jsonResult['weather'][0]['id'])), weatherIsDay)

        embed = Embed(
            title=f'Погода: {city} :flag_{weatherCountry}:', color=0x543964)

        embed.add_field(name='На улице:', value=weatherType +
                        '' + weatherId, inline=False)
        embed.add_field(name='Температура :thermometer:',
                        value=f'{weatherTemp} °C', inline=False)
        embed.add_field(name='Скорость ветра :dash:',
                        value=f'{weatherDirection} {weatherWindSpeed} м/c', inline=False)
        embed.add_field(name='Влажность:droplet:',
                        value=f'{weatherHumidity} %', inline=False)
        embed.set_footer(text='Powered by openweathermap.org')

        await ctx.send(embed=embed)

    async def getWeatherMoji(self, weatherId, weatherIsDay):
        if weatherId.startswith('2'):
            return ':thunder_cloud_rain:'
        elif weatherId.startswith('3'):
            return ':white_sun_rain_cloud:'
        elif weatherId.startswith('5'):
            return ':cloud_rain:'
        elif weatherId.startswith('6'):
            return ':snowflake:'
        elif weatherId.startswith('800'):
            if weatherIsDay:
                return ':sunny:'
            else:
                return ':first_quarter_moon_with_face:'
        elif weatherId.startswith('80'):
            return ':cloud:'
        else:
            return ':question:'

    async def convertWindDirection(self, directionInNumbers):
        # Надеюсь правильно
        possibleDirections = ["Северный", "Северо-Северо-Восточный", "Северо-Восточный", "Восточно-Северо-Восточный",
                              "Восточный", "Восточно-Юго-Восточный", "Юго-Восточный", "Юго-Юго-Восточный",
                              "Южный", "Юго-Юго-Западный", "Юго-Западный", "Западно-Юго-Западный",
                              "Западный", "Западо-Северо-Западный", "Северо-Западный", "Северо-Северо-Западный"]

        value = int((directionInNumbers/22.5) + 0.5)

        return possibleDirections[value % 16]


def setup(bot):
    bot.add_cog(weather(bot))
