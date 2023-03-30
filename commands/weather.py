from discord import Embed
from discord.ext.commands.context import Context
from discord.ext.commands import Cog, command, CommandError, MissingRequiredArgument, hybrid_command
from os import getenv
from dotenv import load_dotenv
from aiohttp import ClientSession
from config import guilds
from .resources.AutomatedMessages import automata

load_dotenv()

name = 'weather'
description = 'Погода по запрашиваемому городу'


class CityNotFound(CommandError):
    pass

class BlankCityName(CommandError):
    pass

class weather(Cog):
    def __init__(self, bot):
        self.bot = bot

    async def cog_command_error(self, ctx, error):
        if isinstance(error, MissingRequiredArgument):
            return await ctx.send(embed=automata.generateEmbErr('Город не указан', error=error))
        if isinstance(error, CityNotFound):
            return await ctx.send(embed=automata.generateEmbErr('Запрашиваемый город не найден', error=error))
        if isinstance(error, BlankCityName):
            return await ctx.send(embed=automata.generateEmbErr('Город не указан', error=error))
        raise error

 
    @hybrid_command(name=name, description=description)
    async def getWeather(self, ctx, city):
        # Получаем токен
        weatherToken = getenv('WEATHER_TOKEN')
        # Ссылка с запросом q=Город appid=Токен
        query = f'https://api.openweathermap.org/data/2.5/weather?q={city}&lang=ru&units=metric&appid={weatherToken}'
        # Получаем инфу из запроса
        async with ClientSession() as session:
            async with session.get(query) as response:
                if(response.status == 404):
                    raise CityNotFound(city)

                # Загружаем запрос в формат JSON
                jsonResult = await response.json()

        # Получаем информацию из JSON, переменные говорят сами за себя
        weatherCountry = jsonResult['sys']['country'].lower()
        weatherType = jsonResult['weather'][0]['description']
        weatherTemp = round(jsonResult['main']['temp'])
        weatherWindSpeed = jsonResult['wind']['speed']
        weatherHumidity = jsonResult['main']['humidity']
        # Функция convertWindDirection конвертирует угловое значение в градусах в словесное направление ветра
        weatherDirection = await self.convertWindDirection((jsonResult['wind']['deg']))

        # Если время в городе больше чем время восхода солнца и меньше захода солнца
        # То в городе день
        if jsonResult['dt'] > jsonResult['sys']['sunrise'] and jsonResult['dt'] < jsonResult['sys']['sunset']:
            weatherIsDay = True
        else:
            weatherIsDay = False

        # Получаем эмодзики исходя из id из запроса
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
        # Направление меняется каждые 22.5 градуса (0.5 чтоб весело жилось)
        value = int((directionInNumbers / 22.5) + 0.5)
        # Возвращаем направление ветра в зависимости от градусов
        return possibleDirections[value % 16]


async def setup(bot):
    await bot.add_cog(weather(bot))
