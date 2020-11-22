from discord.ext import commands
from random import sample
import requests
from PIL import Image
from io import BytesIO


class randImg(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Обработка ошибок
    async def cog_command_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send(error)

    @commands.cooldown(rate=1, per=5)
    @commands.command(name='randImg', description='Отправляет случайное изображение из imgur', aliases=['randimg'])
    async def randImg(self, ctx):
        url = 'https://i.imgur.com/'
        symbols = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'

        # Генерируем 5 рандомных  символов
        randSymbols = ''.join(sample(symbols, 5))

        # Делаем ссылку на картинку
        iImgurUrl = url + randSymbols + '.png'

        # Получаем инфу об картинке
        req = requests.get(iImgurUrl, headers={'User-Agent': 'Mozilla/5.0'})

        # Открываем картинку
        img = Image.open(BytesIO(req.content))

        # Если картинки нет, то она имеет размер 161х81
        if img.size[0] == 161 and img.size[1] == 81:
            # Рекурсивно вызываем функцию пока картинка не будет найдена
            await ctx.invoke(await self.randImg(ctx))
        else:
            # Картинка нашлась, отправляем ссылку на картинку
            await ctx.send(iImgurUrl)


def setup(bot):
    bot.add_cog(randImg(bot))
