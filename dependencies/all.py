from dataclasses import dataclass

from .repository.prefix.abc import PrefixRepository
from .api.youtube_random.abc import  YoutubeRandomApi
from .api.weather.abc import  WeatherAPI
from .api.nasa.abc import NasaAPI

@dataclass
class Dependencies:
    prefix_repo: PrefixRepository
    youtube_random_api: YoutubeRandomApi
    openweather_api: WeatherAPI
    wttr_api: WeatherAPI
    nasa_api: NasaAPI