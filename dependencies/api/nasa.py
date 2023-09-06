from aiohttp import ClientSession

class NasaApi:
    BASE_URL = "https://api.nasa.gov/planetary/apod?api_key=DEMO_KEY"

    async def get_image_of_the_day(self):
        async with ClientSession() as session:
            async with session.get(self.BASE_URL) as response:
                res = await response.json()
                return {
                    'title': res['title'],
                    'image': res['hdurl']
                }