from aiohttp import ClientSession

class WttrAPI:
    def __init__(self):
        self.BASE_URL = "https://ru.wttr.in/"

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
        async with ClientSession() as session:
            async with session.get(f'{self.BASE_URL}/{city}', params={'format': 'j1'}) as response:
                if(response.status == 404):
                    return None

                # Загружаем запрос в формат JSON
                jsonResult = await response.json()

        conds = jsonResult['current_condition'][0]
        
        weatherHumidity = conds['humidity']
        weatherType = conds["lang_ru"][0]['value']
        weatherTemp = conds['temp_C']
        weatherDirection = await self.convertWindDirection(int(conds['winddirDegree']))
        weatherWindSpeed = conds['windspeedKmph']


        weatherCode = conds['weatherCode']

        wwo = WWO_CODE[weatherCode]

        pict = WEATHER_SYMBOL_WEGO[wwo]

        return {
            'city': city, 
            'weatherType': f'{weatherType} {WEATHER_SYMBOL[wwo]}`{pict}`', 
            'temp': weatherTemp, 
            'wind_speed': weatherWindSpeed,
            'wind_direction': weatherDirection, 
            'humidity': weatherHumidity,
            'weatherCountry': jsonResult["nearest_area"][0]['country'][0]['value']
        }


#   https://github.com/chubin/wttr.in/blob/master/lib/constants.py

WWO_CODE = {
    "113": "Sunny",
    "116": "PartlyCloudy",
    "119": "Cloudy",
    "122": "VeryCloudy",
    "143": "Fog",
    "176": "LightShowers",
    "179": "LightSleetShowers",
    "182": "LightSleet",
    "185": "LightSleet",
    "200": "ThunderyShowers",
    "227": "LightSnow",
    "230": "HeavySnow",
    "248": "Fog",
    "260": "Fog",
    "263": "LightShowers",
    "266": "LightRain",
    "281": "LightSleet",
    "284": "LightSleet",
    "293": "LightRain",
    "296": "LightRain",
    "299": "HeavyShowers",
    "302": "HeavyRain",
    "305": "HeavyShowers",
    "308": "HeavyRain",
    "311": "LightSleet",
    "314": "LightSleet",
    "317": "LightSleet",
    "320": "LightSnow",
    "323": "LightSnowShowers",
    "326": "LightSnowShowers",
    "329": "HeavySnow",
    "332": "HeavySnow",
    "335": "HeavySnowShowers",
    "338": "HeavySnow",
    "350": "LightSleet",
    "353": "LightShowers",
    "356": "HeavyShowers",
    "359": "HeavyRain",
    "362": "LightSleetShowers",
    "365": "LightSleetShowers",
    "368": "LightSnowShowers",
    "371": "HeavySnowShowers",
    "374": "LightSleetShowers",
    "377": "LightSleet",
    "386": "ThunderyShowers",
    "389": "ThunderyHeavyRain",
    "392": "ThunderySnowShowers",
    "395": "HeavySnowShowers",
}

WEATHER_SYMBOL = {
    "Unknown":             "✨",
    "Cloudy":              "☁️",
    "Fog":                 "🌫",
    "HeavyRain":           "🌧",
    "HeavyShowers":        "🌧",
    "HeavySnow":           "❄️",
    "HeavySnowShowers":    "❄️",
    "LightRain":           "🌦",
    "LightShowers":        "🌦",
    "LightSleet":          "🌧",
    "LightSleetShowers":   "🌧",
    "LightSnow":           "🌨",
    "LightSnowShowers":    "🌨",
    "PartlyCloudy":        "⛅️",
    "Sunny":               "☀️",
    "ThunderyHeavyRain":   "🌩",
    "ThunderyShowers":     "⛈",
    "ThunderySnowShowers": "⛈",
    "VeryCloudy": "☁️",
}

WEATHER_SYMBOL_WIDTH_VTE = {
    "✨": 2,
    "☁️": 1,
    "🌫": 2,
    "🌧": 2,
    "🌧": 2,
    "❄️": 1,
    "❄️": 1,
    "🌦": 1,
    "🌦": 1,
    "🌧": 1,
    "🌧": 1,
    "🌨": 2,
    "🌨": 2,
    "⛅️": 2,
    "☀️": 1,
    "🌩": 2,
    "⛈": 1,
    "⛈": 1,
    "☁️": 1,
}

WIND_DIRECTION = [
    "↓", "↙", "←", "↖", "↑", "↗", "→", "↘",
]

WEATHER_SYMBOL_WEGO = {
    "Unknown": """
  .-.   
   __)  
  (     
   ˙-’  
    •   
""",
    "Sunny": """
  \\   /  
    .-.    
 ― (   ) ― 
    ˙-˙    
   /   \\  
""",

    "PartlyCloudy":"""
   .-. 
  (   ).
(___(__)
""",
    "Cloudy":""" 
    .--.    
 .-(    ).  
(___.__)__) 
""",
    "VeryCloudy": """ 
    .--.    
 .-(    ).  
(___.__)__) 
""",
    "LightShowers": """
       .-. 
     (    )
  (___(__ )
  ‘ ‘ ‘ ‘  
 ‘ ‘ ‘ ‘   
    """,
    "HeavyShowers": 
"""
       .-. 
     (    )
  (___(__ )
 ‚‘‚‘‚‘‚‘
 ‚’‚’‚’‚’
""",
    "LightSnowShowers": """
       .-. 
     (    )
  (___(__ )
  *  *  *
 *  *  * 
""",

    "HeavySnowShowers": """
       .-. 
     (    )
  (___(__ )
   * * * *
 * * * * 
""",
    "LightSleetShowers": """ 
     .-.   
    (   ). 
  (___(__) 
      ‘  ‘ 
  ‘ ‘      
""",
    "ThunderyShowers": """
     .-.     
    (   ).   
  (___(__)   
 ⚡ ‘ ‘\ ⚡‘ 
   ‘ ‘ ‘ ‘   
""",
    "ThunderyHeavyRain": """ 
     .-.    
    (   ).  
   (___(__) 
 ‚‘ ⚡ ‘‚ ⚡
 ‚’‚’ ⚡’‚’ 
""",
    "ThunderySnowShowers": """ 
     .-.    
    (   ).  
  (___(__)  
  * ⚡ * ⚡ 
 ⚡ *  ⚡ * 
""",
    "LightRain": """
   .-.    
  (   ).  
 (___(__) 
  ‘ ‘ ‘ ‘ 
 ‘ ‘ ‘ ‘  
""",
    "HeavyRain": """
    .-.   
   (   ). 
  (___(__)
‚‘‚‘‚‘‚‘  
‚’‚’‚’‚’  
""",
    "LightSnow": """ 
    .-.    
   (   ).  
  (___(__) 
   *  *  * 
  *  *  *  
""",
    "HeavySnow": """
    .-.   
   (   ). 
  (___(__)
  * * * * 
 * * * *  
""",
    "LightSleet": """
   .-.   
  (   ). 
 (___(__)
  ‘ ‘    
 * ‘ *‘  
""",
    "Fog": """
_ - _ - _ -
 _ - _ - _ 
_ - _ - _ -
    """,
}
