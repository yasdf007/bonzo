from abc import ABC, abstractmethod

class YoutubeRandomRepository(ABC):
    @abstractmethod
    async def get_video_id(self):
        raise NotImplementedError()