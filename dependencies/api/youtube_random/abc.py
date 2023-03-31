from abc import ABC, abstractmethod

class YoutubeRandomApi(ABC):
    @abstractmethod
    async def get_video_id(self):
        raise NotImplementedError()