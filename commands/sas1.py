from discord.ext import commands
from discord import file

name='sas'
descriprion='sas'

class sas(commands.Cog)
    def__init__(self, bot):
        self.bot = bot

        #ну короче он должен раз в <n(рандом)> минут докапываться до рандомного юзера с каверзным вопросом
        #сейчас он вроде как отправляет сообщение без упоминания с одинаковым интервалом
        @commands.command(name=name, descriprion=descriprion)
        async def sas(self, ctx):
                    vopros = random.choice(["в жопу дашь или мать продашь?", "когда дрочешь что бормочешь?", "в жопу раз или вилкой в глаз?"])
        await ctx.send(vopros)
        await asyncio.sleep(100)

def setup(bot):
    bot.add_cog(sas(bot))