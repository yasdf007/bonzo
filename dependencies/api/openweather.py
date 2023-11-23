from aiohttp import ClientSession

class OpenWeatherMapAPI:
    def __init__(self, token: str):
        self.BASE_URL = f'https://api.openweathermap.org/data/2.5/weather?lang=ru&units=metric&appid={token}'
        self.USERAGENT = {
        "Accept": "application/json",
        "Content-Type": "application/json",
    }
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

    async def get_weather_data(self, city):
        async with ClientSession(headers=self.USERAGENT) as session:
            async with session.get(self.BASE_URL, params={'q': city}) as response:
                if(response.status == 404):
                    return None

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
        return {
            'city': city, 
            'weatherType': f'{weatherType} {weatherId}', 
            'temp': weatherTemp, 
            'wind_speed': weatherWindSpeed,
            'wind_direction': weatherDirection, 
            'humidity': weatherHumidity,
            'weatherCountry': weatherCountry
        }
