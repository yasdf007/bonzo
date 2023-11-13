from aiohttp import ClientSession
from random import choice

class RandomtubeAPI:
    USERAGENT = {
        "Accept": "application/json",
        "Content-Type": "application/json",
    }
    URL = "https://api.randomtube.xyz/v1/entries/videos"
    PARAMS = {"board": "b", "chan": "2ch.hk", "page": 1}
    
    async def get_random_url(self):
        async with ClientSession(headers=self.USERAGENT) as session:
            async with session.get(self.URL, params=self.PARAMS) as response:
                res = await response.json()

        return choice(res["items"])["url"]