import discord
import lavalink
from discord.ext import commands
import re
import os
from dotenv import load_dotenv

url_rx = re.compile(r'https?://(?:www\.)?.+')

load_dotenv()

class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        if not hasattr(bot, 'lavalink'):
            bot.lavalink = lavalink.Client(bot.user.id)
            lavapassword = os.getenv('LAVAPASS')
            # Host, Port, Password, Region, Name
            bot.lavalink.add_node('185.43.7.82', 2333, str(lavapassword), 'eu', 'music')
            bot.add_listener(bot.lavalink.voice_update_handler,
                             'on_socket_response')

    ######## ----- БЕЗ ЭТОГО НИЧЕ НЕ РАБОТАЕТ НЕ ХОЧУ РАЗБИРАТЬСЯ ПОЧЕМУ ----- ########

    async def cog_before_invoke(self, ctx):
        """ Command before-invoke handler. """
        guild_check = ctx.guild is not None
        #  This is essentially the same as `@commands.guild_only()`
        #  except it saves us repeating ourselves (and also a few lines).

        if guild_check:
            await self.ensure_voice(ctx)
            #  Ensure that the bot and command author share a mutual voicechannel.

        return guild_check

    async def cog_command_error(self, ctx, error):
        if isinstance(error, commands.CommandInvokeError):
            await ctx.send(error.original)
            # The above handles errors thrown in this cog and shows them to the user.
            # This shouldn't be a problem as the only errors thrown in this cog are from `ensure_voice`
            # which contain a reason string, such as "Join a voicechannel" etc. You can modify the above
            # if you want to do things differently.

    ######## ----- БЕЗ ЭТОГО НИЧЕ НЕ РАБОТАЕТ НЕ ХОЧУ РАЗБИРАТЬСЯ ПОЧЕМУ ----- ########

    async def ensure_voice(self, ctx):
        """ Чекает бота и автора команды на войс. """
        # Создает плеер
        player = self.bot.lavalink.player_manager.create(
            ctx.guild.id, endpoint=str(ctx.guild.region))

        # Эти команды нужны для захода бота  в войс
        should_connect = ctx.command.name in ('play',)

        if not ctx.author.voice or not ctx.author.voice.channel:
            # cog_command_error handler ловит ошибку.
            raise commands.CommandInvokeError('Join a voicechannel first.')

        if not player.is_connected:
            if not should_connect:
                raise commands.CommandInvokeError('Not connected.')

            permissions = ctx.author.voice.channel.permissions_for(ctx.me)

            # Чекам возможность бота зайти в войс и играть музыку
            if not permissions.connect or not permissions.speak:
                raise commands.CommandInvokeError(
                    'I need the `CONNECT` and `SPEAK` permissions.')

            player.store('channel', ctx.channel.id)
            await self.connect_to(ctx.guild.id, str(ctx.author.voice.channel.id))
        else:
            if int(player.channel_id) != ctx.author.voice.channel.id:
                raise commands.CommandInvokeError(
                    'You need to be in my voicechannel.')

    async def connect_to(self, guild_id: int, channel_id: str):
        """ Заходит в войс по ID. channel_id `None` значит дисконнект. """
        ws = self.bot._connection._get_websocket(guild_id)
        await ws.voice_state(str(guild_id), channel_id)

    @commands.command(aliases=['p'])
    async def play(self, ctx, *, query: str):
        """ Ищет и проигрывает музыку исходя из запроса. """

        player = self.bot.lavalink.player_manager.get(ctx.guild.id)

        # Чекаем на ссылку, если не ссылка то поиск по словам
        if not url_rx.match(query):
            query = f'ytsearch:{query}'

        results = await player.node.get_tracks(query)

        if not results or not results['tracks']:
            return await ctx.send('Nothing found!')

        embed = discord.Embed(color=discord.Color.blurple())

        # Типы loadTypes:
        #   TRACK_LOADED    - Одно видео или ссылка на видео
        #   PLAYLIST_LOADED - Прямая ссылка на плейлист
        #   SEARCH_RESULT   - Запрос по словам.
        #   NO_MATCHES      - Не нашло
        #   LOAD_FAILED     - Ошибка во время загрузки (возможно)

        if results['loadType'] == 'PLAYLIST_LOADED':
            tracks = results['tracks']
            for track in tracks:
                # Добавить все треки из плейлиста в очередь
                player.add(requester=ctx.author.id, track=track)

            embed.title = 'Плейлист загружен!'
            embed.description = f'{results["playlistInfo"]["name"]} - {len(tracks)} треков'

        if results['loadType'] == 'TRACK_LOADED':
            track = results['tracks'][0]
            embed.title = 'Трек загружен'
            embed.description = f'[{track["info"]["title"]}]({track["info"]["uri"]})'
            track = lavalink.models.AudioTrack(
                track, ctx.author.id, recommended=True)
            player.add(requester=ctx.author.id, track=track)

        if results['loadType'] == 'SEARCH_RESULT':
            i = 0
            query_result = ''
            tracks = results['tracks'][0:10]
            for track in tracks:
                i += 1
                query_result += f'{i}) {track["info"]["title"]} \n'

            embed = discord.Embed()
            embed.title = 'Выбери трек'
            embed.description = query_result
            await ctx.send(embed=embed)

            # Проверяем того, кто отправил запрос и кто ответил
            # Ждем того, кто запросил
            def check(m):
                return m.author.id == ctx.author.id

            user_respone = await self.bot.wait_for('message', check=check)

            embed = discord.Embed()
            # Проверяем цифру ли отправил юзер и добавляем трек в очередь
            try:
                track = tracks[int(user_respone.content)-1]
                player.add(requester=ctx.author.id, track=track)
                embed.description = f'**Playing** {track["info"]["title"]}'
            except ValueError:
                embed.title = 'Ты лох'
                embed.description = 'Нужно выбрать цифру из списка, закажи заново'

        await ctx.send(embed=embed)

        # Если музыка уже играет, то не подрубаем
        # Иначе будет скип музыки
        if not player.is_playing:
            await player.play()

    @commands.command(aliases=['dc'])
    async def disconnect(self, ctx):
        """ Отрубается и чистит очередь. """

        player = self.bot.lavalink.player_manager.get(ctx.guild.id)

        if not player.is_connected:
            # Не в войсе
            return await ctx.send('Не подрублен в войс')

        if not ctx.author.voice or (player.is_connected and ctx.author.voice.channel.id != int(player.channel_id)):

            # Защита от абуза. Юзер не в войсе или в войсе, но в разных каналах с ботом
            # Из-за чего бот может не отрубиться
            return await ctx.send('You\'re not in my voicechannel!')

        # Удаляем старые треки, чтобы страрые треки не играли, когда кто-то ставит в очередь музыку
        player.queue.clear()

        # Останавливает трек, который играет
        await player.stop()

        # Отрубаемся из войса
        await self.connect_to(ctx.guild.id, None)
        await ctx.send('Disconnected.')


def setup(bot):
    bot.add_cog(Music(bot))
