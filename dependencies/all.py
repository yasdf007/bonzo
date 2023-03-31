from dataclasses import dataclass

from .repository.prefix.abc import PrefixRepository
from .api.youtube_random.abc import  YoutubeRandomApi

@dataclass
class Dependencies:
    prefix_repo: PrefixRepository
    youtube_random_api: YoutubeRandomApi