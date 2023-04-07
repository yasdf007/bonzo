from discord import Embed
from discord.ext.commands import Cog, hybrid_command, Context
from bot import Bot

name = "invite"
description = "Ссылка на приглашение бота"
invlink = "https://discord.com/api/oauth2/authorize?client_id=680132907859443790&permissions=8&scope=bot%20applications.commands"


class invite(Cog):
    def __init__(self, bot):
        self.bot: Bot = bot

    # функция, отправляющая инвайт-ссылку бота в чат
    @hybrid_command(name=name, description=description)
    async def invite(self, ctx: Context):
        embedd = Embed(title="**Зовём /bonzo/ на Ваш сервер...**", colour=0xB84000)
        embedd.set_thumbnail(url="https://i.ibb.co/Xk7qTy4/BOnzo-1.png")
        embedd.add_field(
            name="Спасибо за поддержку!",
            value=f"**-->** [Нажмите сюда!]({invlink}) **<--**",
        )
        embedd.set_footer(text="/by bonzo/ for @" + ctx.author.name)
        await ctx.send(embed=embedd)


async def setup(bot):
    await bot.add_cog(invite(bot))
