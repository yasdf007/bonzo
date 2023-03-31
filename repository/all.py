from dataclasses import dataclass

from .prefix.abc import PrefixRepository

@dataclass
class Repositories:
    prefix_repo: PrefixRepository