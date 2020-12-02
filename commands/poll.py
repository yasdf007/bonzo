from discord import Embed
from discord.ext import commands
from datetime import datetime, timedelta

from discord.ext import tasks


class Poll(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.emojis = ['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣']
        self.pollIds = []

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if payload.message_id in (poll[1] for poll in self.pollIds):
            message = await self.bot.get_channel(payload.channel_id).fetch_message(payload.message_id)

            for reaction in message.reactions:
                if (not payload.member.bot
                    and payload.member in await reaction.users().flatten()
                        and reaction.emoji != payload.emoji.name):
                    await message.remove_reaction(reaction.emoji, payload.member)

    @commands.command(name='poll', description='Выборы')
    async def poll(self, ctx, seconds: int, question: str, *options):
        if len(options) > 6:
            await ctx.send('Максимум 6 значений')
            return

        embed = Embed(title=question, color=0xff0000,
                      timestamp=datetime.utcnow())

        embed.add_field(name='Варинаты',
                        value='\n'.join(
                            [f'{self.emojis[index]} {option}' for index, option in enumerate(options)]))
        message = await ctx.send(embed=embed)

        for emoji in self.emojis[:len(options)]:
            await message.add_reaction(emoji)

        self.pollIds.append((message.channel.id, message.id))

    async def pollComplete(self):
        embed = Embed(title='Ниче не работает',
                      color=0xff0000, timestamp=datetime.utcnow())

        message = await self.bot.get_channel(681179689775398943)

        await message.channel.send(embed=embed)


def setup(bot):
    bot.add_cog(Poll(bot))
