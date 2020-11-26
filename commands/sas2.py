from discord.ext import commands
from discord import file

name='sas'
descriprion='sas'

class sas(commands.Cog)
    def__init__(self, bot):
        self.bot = bot

        #ну короче по плану он должен раз в <n(рандом)> минут докапываться до рандомного юзера с каверзным вопросом
        #сейчас он вроде как отправляет сообщение, но без упоминания
        @commands.command(name=name, descriprion=descriprion)
        async def sas(self, ctx):
                    vopros = random.choice(["в жопу дашь или мать продашь?", "когда дрочешь что бормочешь?", "в жопу раз или вилкой в глаз?"])
                    ouch = random.randint(100,300)
        await ctx.send(vopros)
        await asyncio.sleep(ouch)

def setup(bot):
    bot.add_cog(sas(bot))