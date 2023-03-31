from dataclasses import dataclass
from .prefix import PrefixRepositoryMemory, PrefixRepository

@dataclass
class Repositories:
    prefix_repo: PrefixRepository