from dataclasses import dataclass

from .prefix.abc import PrefixRepository
from .youtube_random.abc import  YoutubeRandomRepository

@dataclass
class Repositories:
    prefix_repo: PrefixRepository
    youtube_random_repo: YoutubeRandomRepository