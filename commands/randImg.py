from discord.ext.commands import Cog, CommandOnCooldown, command, cooldown, BucketType
from bonzoboot import slash, guilds
from random import sample
from aiohttp import ClientSession
from PIL import Image
from io import BytesIO

name = 'randImg'
description = 'Отправляет случайное изображение из imgur'


class randImg(Cog):
    def __init__(self, bot):
        self.bot = bot

    # Обработка ошибок
    async def cog_command_error(self, ctx, error):
        if isinstance(error, CommandOnCooldown):
            await ctx.message.reply(error)

    @cooldown(rate=1, per=5, type=BucketType.user)
    @slash.slash(name=name, description=description, guild_ids=guilds)
    async def randImg(self, *ctx):
        url = 'https://i.imgur.com/'
        symbols = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'

        # Генерируем 5 рандомных  символов
        randSymbols = ''.join(sample(symbols, 5))

        # Делаем ссылку на картинку
        iImgurUrl = url + randSymbols + '.png'

        # Получаем инфу об картинке
        async with ClientSession() as session:
            async with session.get(iImgurUrl) as response:
                res = await response.read()

        # Открываем картинку
        img = Image.open(BytesIO(res))

        # Если картинки нет, то она имеет размер 161х81
        if img.size[0] == 161 and img.size[1] == 81:
            # Рекурсивно вызываем функцию пока картинка не будет найдена
            await self.send("Возникла непредвиденная ошибка. Попробуйте снова")
        else:
            # Картинка нашлась, отправляем ссылку на картинку
            await self.send(iImgurUrl)


def setup(bot):
    bot.add_cog(randImg(bot))
