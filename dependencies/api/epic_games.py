from aiohttp import ClientSession
from datetime import datetime


link = "https://store-site-backend-static.ak.epicgames.com/freeGamesPromotions"

async def get_free_games():
    games_data = []

    params = {'locale': 'ru', 'country': 'RU', 'allowCountries': 'RU'}
    async with ClientSession() as session:
        async with session.get(link, params=params) as response:
            res = await response.json()

    games = res["data"]["Catalog"]["searchStore"]["elements"]

    for game in games:
        promotions = game["promotions"]

        if not promotions:
            continue

        if len(promotions["promotionalOffers"]) == 0:
            continue

        freeDiscountSetting = promotions["promotionalOffers"][0][
            "promotionalOffers"
        ][0]["discountSetting"]["discountPercentage"]

        if freeDiscountSetting != 0:
            continue

        due_date = datetime.fromisoformat(
            promotions["promotionalOffers"][0]["promotionalOffers"][0]["endDate"][
                :-1
            ]
        ).strftime("%d/%m/%Y")

        game_name = game["title"]

        slug = game["catalogNs"]['mappings'][0]['pageSlug']

        game_link = "https://www.epicgames.com/store/ru/p/" + slug

        game_photo_url = game['keyImages'][0]['url']

        price_before = game['price']['totalPrice']['fmtPrice']['originalPrice']

        games_data.append(
            {
                'name': game_name,
                'price_before': price_before,
                'due_date': due_date,
                'game_photo_url': game_photo_url,
                'link_to_game': game_link
            }
        )

    return games_data