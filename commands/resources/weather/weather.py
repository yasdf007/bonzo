from dependencies.api.openweather       import OpenWeatherMapAPI
from dependencies.api.wttr              import WttrAPI
from os       import getenv

providers = {
    'openweather': OpenWeatherMapAPI(getenv("WEATHER_TOKEN")),
    'wttr': WttrAPI()
}

def get_provider(provider_name: str):
    return providers.get(provider_name, providers['openweather'])
