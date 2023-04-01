from .abc import CryptoAPI, Response
from aiohttp import ClientSession

class CoinmarketcapAPI(CryptoAPI):
        LISTINGS_URL = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest"

        def __init__(self, token: str):
            self.HEADERS = {
                "Accept": "application/json",
                "Content-Type": "application/json",
                "Accept-Encoding": "deflate, gzip",
                "X-CMC_PRO_API_KEY": token,
            }
        

        async def get_biggest_currencies(self):
            params = {"start": "1", "limit": "10", "convert": "USD"}
            async with ClientSession(headers=self.HEADERS) as session:
                async with session.get(self.LISTINGS_URL, params=params) as response:
                    res = (await response.json())["data"]

            return list(map(
                lambda info: Response(
                    name=info['name'],
                    symbol=info['symbol'],
                    price_usd=info["quote"]["USD"]["price"]),
                    res
                ))

