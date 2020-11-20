import discord
from discord.ext import commands


class helpcmd(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def help(self, ctx):
        embed = discord.Embed(
            title='**Команды бота:**',  # title - головная часть, colour - hex-код цвета полоски
            colour=0xffff00)
        embed.set_thumbnail(
            url='https://i.ibb.co/Xk7qTy4/BOnzo-1.png')
        # inline отвечает за смещение вправо (репрезентация в одной строке)
        embed.add_field(
            name='ping', value='Понг!', inline=False)
        embed.add_field(
            name='roll', value='Ролит как в доте или между двумя числами', inline=False)
        embed.add_field(
            name='randomcat', value='Отправляет случайного котика :3', inline=False)
        embed.add_field(
            name='pict', value='Отправляет случайное изображение из prnt.sc :o', inline=False)
        embed.add_field(
            name='randImg', value='Отправляет случайное изображение из imgur', inline=False)
        embed.add_field(
            name='serverinfo', value='Показывает информацию о сервере (BETA)', inline=False)
        embed.add_field(
            name='clear', value='Очищает последние x сообщений (только для разработчиков)', inline=False)
        embed.add_field(
            name='evala', value='Исполняет код. (только для создателей бота)', inline=False)
        embed.add_field(
            name='obser', value='Виды обсёров.......', inline=False)
        embed.add_field(
            name='weather/погода', value='Погода по запрашиваемому городу (BETA)', inline=False)
        embed.add_field(
            name='info', value='Выдаёт информацию по пользователю (BETA)', inline=False)

        #  embed.add_field(name='', value='', inline=)
        embed.set_footer(text=f"/by bonzo/ for {ctx.message.author}",
                         icon_url=ctx.message.author.avatar_url)  # подпись внизу
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(helpcmd(bot))
