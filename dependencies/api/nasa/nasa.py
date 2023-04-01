from .abc import NasaAPI, Response
from aiohttp import ClientSession

class NasaApi(NasaAPI):
    BASE_URL = "https://api.nasa.gov/planetary/apod?api_key=DEMO_KEY"

    async def get_response(self) -> Response:
        async with ClientSession() as session:
            async with session.get(self.BASE_URL) as response:
                res = await response.json()

            return Response(title=res['title'], image=res['hdurl'])