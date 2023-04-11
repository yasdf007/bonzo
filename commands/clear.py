from discord import TextChannel
from discord.ext.commands import Cog, has_permissions, bot_has_permissions, hybrid_command, Context


from bot import Bot

name = "clear"
description = "Очищает последние x сообщений (для персонала сервера)"


class Clear(Cog):
    def __init__(self, bot):
        self.bot: Bot = bot

    # функция, удаляющая X сообщений из чата
    @hybrid_command(name=name, description=description)
    @has_permissions(manage_messages=True)
    @bot_has_permissions(manage_messages=True)
    async def clear(self, ctx: Context, count: int):
        # удаляем запрошенное кол-во сообщений!
        await TextChannel.purge(ctx.message.channel, limit=count + 1, bulk=True)
        # отправляем отчёт и удаляем его через 5 секунд
        msg = await ctx.send(f"Очистил {count} сообщений!", delete_after=5)

async def setup(bot):
    await bot.add_cog(Clear(bot))
