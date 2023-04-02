from abc import ABC, abstractmethod

class FreeGamesRepository(ABC):
    db = None
    @abstractmethod
    async def get_channel(self, channel_id: int):
        raise NotImplementedError()

    async def get_channels(self):
        raise NotImplementedError()

    @abstractmethod
    async def insert_channel(self, guild_id: int, channel_id: int):
        raise NotImplementedError()

    @abstractmethod
    async def delete_channel(self, guild_id: int):
        raise NotImplementedError()