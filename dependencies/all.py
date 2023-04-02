from dataclasses import dataclass

from .repository.prefix.abc import PrefixRepository
from .repository.free_games.abc import FreeGamesRepository
from .repository.member_info.abc import MemberHandlerRepository
from .api.youtube_random.abc import  YoutubeRandomApi
from .api.weather.abc import  WeatherAPI
from .api.nasa.abc import NasaAPI
from .api.dvach.abc import DvachAPI
from .api.crypto.abc import CryptoAPI
from .api.free_games.abc import FreeGamesAPI

@dataclass
class Dependencies:
    prefix_repo: PrefixRepository
    free_games_repo: FreeGamesRepository
    members_repo: MemberHandlerRepository
    youtube_random_api: YoutubeRandomApi
    openweather_api: WeatherAPI
    wttr_api: WeatherAPI
    nasa_api: NasaAPI
    dvach_api: DvachAPI
    crypto_api: CryptoAPI
    free_games_api: FreeGamesAPI