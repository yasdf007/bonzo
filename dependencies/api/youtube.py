import json
from random import choice
from string import digits, ascii_uppercase
from aiogoogle import Aiogoogle  


class YoutubeRandomApiSDK:
    def __init__(self, YOUTUBE_API_KEY):
        self.YOUTUBE_API_KEY = YOUTUBE_API_KEY

    async def get_random_video(self):
        youtubeVideoId = await self.get_video_id()
        return f"https://www.youtube.com/watch?v={youtubeVideoId}"

    async def get_video_id(self):
        youtubeVideoId = ""

        query2 = "".join(choice(ascii_uppercase + digits) for _ in range(4))

        async with Aiogoogle(api_key=self.YOUTUBE_API_KEY) as aiogoogle:
            yt_api  = await aiogoogle.discover('youtube', 'v3')
            req = yt_api.search.list(q=query2, part="id")
            res = await aiogoogle.as_api_key(req)
            requestJSON = json.loads(json.dumps(res))

            # Для каждого результата
            for searchResult in requestJSON["items"]:
                # Выбираем видос (может быть плейлист, но нужен видос)
                if searchResult["id"]["kind"] == "youtube#video":
                    # Сохраняем ID видоса
                    youtubeVideoId = searchResult["id"]["videoId"]

            return youtubeVideoId