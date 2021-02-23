from discord import Embed
from discord.ext.commands import Cog, MissingRole, has_any_role, command
from datetime import datetime, timedelta


class Poll(Cog):
    def __init__(self, bot):
        self.bot = bot
        self.emojis = ['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣']
        self.pollIds = []

    async def cog_command_error(self, ctx, error):
        if isinstance(error, MissingRole):
            await ctx.message.reply('**слыш,** тебе нельзя такое исполнять')

    @Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if payload.message_id in (poll[1] for poll in self.pollIds):
            message = await self.bot.get_channel(payload.channel_id).fetch_message(payload.message_id)

            for reaction in message.reactions:
                if (not payload.member.bot
                    and payload.member in await reaction.users().flatten()
                        and reaction.emoji != payload.emoji.name):
                    await message.remove_reaction(reaction.emoji, payload.member)

    @command(name='poll', description='Выборы (только для разрабов, персоны клуба)')
    @has_any_role('bonzodev', 'Персона Клуба')
    async def poll(self, ctx, seconds: int, question: str, *options):
        await ctx.message.delete()
        if len(options) > len(self.emojis):
            await ctx.message.reply(f'Максимум {len(self.emojis)} значений')
            return

        embed = Embed(title=question, color=0xff0000,
                      timestamp=datetime.utcnow())

        embed.add_field(name='Варинаты',
                        value='\n'.join(
                            [f'{self.emojis[index]} {option}' for index, option in enumerate(options)]))

        message = await ctx.message.reply(embed=embed)

        for emoji in self.emojis[:len(options)]:
            await message.add_reaction(emoji)

        self.pollIds.append((message.channel.id, message.id))

        self.bot.scheduler.add_job(self.pollComplete, "date", run_date=datetime.now(
        ) + timedelta(seconds=seconds), args=[message.channel.id, message.id])

    async def pollComplete(self, channel_id, message_id):
        embed = Embed(title='Выборы окончены',
                      color=0xff0000, timestamp=datetime.utcnow())

        message = await self.bot.get_channel(channel_id).fetch_message(message_id)
        await message.delete()
        # получаем ембед с сообщения голосовлки
        res = message.embeds[0].fields[0].value.split('\n')
        # у кого больше голосов
        most_voted = max(message.reactions, key=lambda x: x.count)
        # получаем значение у кого болльше голосов
        win = next((s for s in res if most_voted.emoji in s))[3:]

        embed.add_field(
            name='Результаты', value=f'Победа {win} с количеством голосов {most_voted.count-1}')

        await message.channel.send(embed=embed)
        self.pollIds.remove((message.channel.id, message.id))


def setup(bot):
    bot.add_cog(Poll(bot))
