from .abc import YoutubeRandomApi
import json
from random import choice
from string import digits, ascii_uppercase
from googleapiclient.discovery import build

class YoutubeRandomApiSDK(YoutubeRandomApi):
    def __init__(self, YOUTUBE_API_KEY):
        YOUTUBE_API_KEY = YOUTUBE_API_KEY
        API_SERVICE_NAME = "youtube"
        API_VERSION = "v3"
        videoNameStart = ["IMG_"]
        videoNameEnd = [".mp4"]

        self.youtube = build(
            API_SERVICE_NAME, API_VERSION, developerKey=YOUTUBE_API_KEY
        )

    async def get_video_id(self):
        youtubeVideoId = ""

        query2 = "".join(choice(ascii_uppercase + digits) for _ in range(4))
        request =self.youtube.search().list(q=query2, maxResults=25, part="id").execute()
        requestJSON = json.loads(json.dumps(request))

        # Для каждого результата
        for searchResult in requestJSON["items"]:
            # Выбираем видос (может быть плейлист, но нужен видос)
            if searchResult["id"]["kind"] == "youtube#video":
                # Сохраняем ID видоса
                youtubeVideoId = searchResult["id"]["videoId"]

        return youtubeVideoId