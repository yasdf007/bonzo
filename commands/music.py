import discord
from discord.embeds import Embed
import lavalink
from discord.ext.commands import Cog, CommandInvokeError, command
from re import compile
from os import getenv
from dotenv import load_dotenv
from time import strftime, gmtime
from random import shuffle

url_rx = compile(r'https?://(?:www\.)?.+')
load_dotenv()

playName = 'play'
playDescription = 'Проигрывает музыку по запросу'
dcName = 'disconnect'
dcDescription = 'Останавливает воспроизведение'

#            bot.lavalink.add_node('localhost', 5000,
#   '', 'eu', 'music')


class Music(Cog):
    def __init__(self, bot):
        self.bot = bot

        if not hasattr(bot, 'lavalink'):
            bot.lavalink = lavalink.Client(bot.user.id)
            lavapassword = getenv('LAVAPASS')
            # Host, Port, Password, Region, Name
            bot.lavalink.add_node('185.43.7.82', 2333,
                                  str(lavapassword), 'eu', 'music')
            bot.add_listener(bot.lavalink.voice_update_handler,
                             'on_socket_response')

        lavalink.add_event_hook(self.track_hook)

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
        if isinstance(error, CommandInvokeError):
            await ctx.send(error.original)
            # The above handles errors thrown in this cog and shows them to the user.
            # This shouldn't be a problem as the only errors thrown in this cog are from `ensure_voice`
            # which contain a reason string, such as "Join a voicechannel" etc. You can modify the above
            # if you want to do things differently.

    async def ensure_voice(self, ctx):
        """ Чекает бота и автора команды на войс. """
        # Создает плеер
        player = self.bot.lavalink.player_manager.create(
            ctx.guild.id, endpoint=str(ctx.guild.region))

        # Эти команды нужны для захода бота  в войс
        should_connect = ctx.command.name in ('play',)

        if not ctx.author.voice or not ctx.author.voice.channel:
            # cog_command_error handler ловит ошибку.
            raise CommandInvokeError('Join a voicechannel first.')

        if not player.is_connected:
            if not should_connect:
                raise CommandInvokeError('Not connected.')

            permissions = ctx.author.voice.channel.permissions_for(ctx.me)

            # Чекам возможность бота зайти в войс и играть музыку
            if not permissions.connect or not permissions.speak:
                raise CommandInvokeError(
                    'I need the `CONNECT` and `SPEAK` permissions.')

            player.store('channel', ctx.channel.id)
            await self.connect_to(ctx.guild.id, str(ctx.author.voice.channel.id))
        else:
            if int(player.channel_id) != ctx.author.voice.channel.id:
                raise CommandInvokeError(
                    'You need to be in my voicechannel.')

    async def track_hook(self, event):
        if isinstance(event, lavalink.events.QueueEndEvent):
            # When this track_hook receives a "QueueEndEvent" from lavalink.py
            # it indicates that there are no tracks left in the player's queue.
            # To save on resources, we can tell the bot to disconnect from the voicechannel.
            guild_id = int(event.player.guild_id)
            await self.connect_to(guild_id, None)

    @Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if member.bot:
            return

        # получаем инстанс музыки
        player = self.bot.lavalink.player_manager.get(member.guild.id)

        # если есть инстанс И есть канал куда он подрублен
        if player and player.channel_id:
            # получаем инфу канала, где подрублен
            channelInfo = self.bot.get_channel(int(player.channel_id))
            #              Если чел вышел             ИЛИ            Сменил канал
            if (before.channel and not after.channel) or (before.channel.id != after.channel.id):
                # Проверяем количество челов в канале с ботом
                # Если бот остался один
                if len(channelInfo.members) <= 1:
                    # Отрубаемся (аналогия функции stop (disconnect, dc))
                    player.queue.clear()
                    await player.stop()
                    await self.connect_to(member.guild.id, None)
        # иначе ничего
        else:
            return

        return

    async def connect_to(self, guild_id: int, channel_id: str):
        """ Заходит в войс по ID. channel_id `None` значит дисконнект. """
        ws = self.bot._connection._get_websocket(guild_id)
        await ws.voice_state(str(guild_id), channel_id)

    @command(name=playName, description=playDescription, aliases=['p'])
    async def play(self, ctx, *, query: str):
        """ Ищет и проигрывает музыку исходя из запроса. """

        player = self.bot.lavalink.player_manager.get(ctx.guild.id)

        # Чекаем на ссылку, если не ссылка то поиск по словам
        if not url_rx.match(query):
            query = f'ytsearch:{query}'

        results = await player.node.get_tracks(query)

        if not results or not results['tracks']:
            return await ctx.send('Nothing found!')

        embed = discord.Embed(color=discord.Color.dark_theme())

        # Типы loadTypes:
        #   TRACK_LOADED    - Одно видео или ссылка на видео
        #   PLAYLIST_LOADED - Прямая ссылка на плейлист
        #   SEARCH_RESULT   - Запрос по словам.
        #   NO_MATCHES      - Не нашло
        #   LOAD_FAILED     - Ошибка во время загрузки (возможно)

        if results['loadType'] == 'PLAYLIST_LOADED':
            trackLength = 0
            tracks = results['tracks']

            for track in tracks:
                trackLength += (track['info']['length']) // 1000

                # Добавить все треки из плейлиста в очередь
                player.add(requester=ctx.author.id, track=track)
            embed.set_author(
                name='Плейлист загружен!', icon_url=ctx.author.avatar_url)

            embed.add_field(
                name='Название', value=f'`{results["playlistInfo"]["name"]}`', inline=False)

            trackLength = strftime(
                '%H:%M:%S', gmtime(trackLength))
            embed.add_field(name='Загружено',
                            value=f'`{len(tracks)} треков`', inline=True)

            embed.add_field(name='Длительность',
                            value=f'`{trackLength}`', inline=True)

        if results['loadType'] == 'TRACK_LOADED':
            track = results['tracks'][0]

            embed.set_author(
                name='Добавил в очередь', icon_url=ctx.author.avatar_url)

            embed.add_field(
                name='Название', value=f'[{track["info"]["title"]}]({track["info"]["uri"]})', inline=False)

            trackLength = strftime(
                '%M:%S', gmtime((track["info"]["length"]) // 1000))
            embed.add_field(name='Длительность',
                            value=f'{trackLength}', inline=True)

            embed.set_thumbnail(
                url=f'https://img.youtube.com/vi/{track["info"]["identifier"]}/0.jpg')

            track = lavalink.models.AudioTrack(
                track, ctx.author.id, recommended=True)
            player.add(requester=ctx.author.id, track=track)

        if results['loadType'] == 'SEARCH_RESULT':
            query_result = ''
            tracks = results['tracks'][0:10]
            for id, track in enumerate(tracks, 1):
                query_result += f'`{id})` {track["info"]["title"]} \n'

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
                track = tracks[int(user_respone.content) - 1]
                player.add(requester=ctx.author.id, track=track)

                embed.set_author(
                    name='Добавил в очередь', icon_url=ctx.author.avatar_url)

                embed.add_field(
                    name='Название', value=f'[{track["info"]["title"]}]({track["info"]["uri"]})', inline=False)

                trackLength = strftime(
                    '%M:%S', gmtime((track["info"]["length"]) // 1000))
                embed.add_field(name='Длительность',
                                value=f'{trackLength}', inline=True)

                embed.set_thumbnail(
                    url=f'https://img.youtube.com/vi/{track["info"]["identifier"]}/0.jpg')
            except:
                embed.title = 'Ты лох'
                embed.description = 'Нужно выбрать цифру из списка, закажи заново'

        await ctx.send(embed=embed)

        # Если музыка уже играет, то не подрубаем
        # Иначе будет скип музыки
        if not player.is_playing:
            await player.play()

    @command(name=dcName, description=dcDescription, aliases=['dc', 'leave'])
    async def stop(self, ctx):
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

    @command(name='queue', description='Показывает очередь (до 10 треков)')
    async def queue(self, ctx):
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)

        if not player.is_connected:
            # Не в войсе
            return await ctx.send('Не подрублен в войс')

        if not ctx.author.voice or (player.is_connected and ctx.author.voice.channel.id != int(player.channel_id)):
            # Защита от абуза. Юзер не в войсе или в войсе, но в разных каналах с ботом
            return await ctx.send('You\'re not in my voicechannel!')

        if len(player.queue) > 0:
            result = ''
            embed = discord.Embed(title='Треки в очереди',
                                  color=discord.Color.dark_theme())
            embed.set_footer(
                text=f'Всего в очереди {len(player.queue)} треков')

            for id, track in enumerate(player.queue[0:10], 1):
                result += f'{id}) {track.title} \n'

            embed.description = result
            await ctx.send(embed=embed)
        else:
            await ctx.send('Очередь пустая')
        return

    @command(name='volume', description='Изменяет громкость (до 1000)')
    async def volume(self, ctx, vol: int):
        if vol > 1000:
            await ctx.send(embed=Embed(title='Оглохнешь емое че творишь', color=discord.Color.dark_theme()))
            return
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)

        if not player.is_connected:
            # Не в войсе
            return await ctx.send('Не подрублен в войс')

        if not ctx.author.voice or (player.is_connected and ctx.author.voice.channel.id != int(player.channel_id)):
            # Защита от абуза. Юзер не в войсе или в войсе, но в разных каналах с ботом
            return await ctx.send('You\'re not in my voicechannel!')

        try:
            await player.set_volume(vol)
            embed = discord.Embed(
                title=f'Громоксть теперь {vol}', color=discord.Color.dark_theme())
            await ctx.send(embed=embed)
        except:
            raise CommandInvokeError('Ошибка при изменении громкости')
        return

    @command(name='skip', description='Скипает к следующему треку в очереди (если есть)')
    async def skip(self, ctx):
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)

        if not player.is_connected:
            # Не в войсе
            return await ctx.send('Не подрублен в войс')

        if not ctx.author.voice or (player.is_connected and ctx.author.voice.channel.id != int(player.channel_id)):
            # Защита от абуза. Юзер не в войсе или в войсе, но в разных каналах с ботом
            return await ctx.send('You\'re not in my voicechannel!')

        try:
            embed = discord.Embed(
                title=f'{player.current.title} `Скипнут`', color=discord.Color.dark_theme())

            await player.skip()

            await ctx.send(embed=embed)
        except:
            raise CommandInvokeError('Ошибка при скипе')

        return

    @command(name='pause', description='Паузит/анпаузит музыку')
    async def pause(self, ctx):

        player = self.bot.lavalink.player_manager.get(ctx.guild.id)

        if not player.is_connected:
            # Не в войсе
            return await ctx.send('Не подрублен в войс')

        if not ctx.author.voice or (player.is_connected and ctx.author.voice.channel.id != int(player.channel_id)):
            # Защита от абуза. Юзер не в войсе или в войсе, но в разных каналах с ботом
            return await ctx.send('You\'re not in my voicechannel!')

        try:
            if player.paused:
                await player.set_pause(False)
            else:
                await player.set_pause(True)
        except:
            raise CommandInvokeError('Ошибка при паузе')
        return

    @command(name='shuffle', description='Проигрывает очередь в случайном порядке')
    async def _shuffle(self, ctx):

        player = self.bot.lavalink.player_manager.get(ctx.guild.id)

        if not player.is_connected:
            # Не в войсе
            return await ctx.send('Не подрублен в войс')

        if not ctx.author.voice or (player.is_connected and ctx.author.voice.channel.id != int(player.channel_id)):
            # Защита от абуза. Юзер не в войсе или в войсе, но в разных каналах с ботом
            return await ctx.send('You\'re not in my voicechannel!')

        try:
            shuffle(player.queue)
        except:
            raise CommandInvokeError('Ошибка при шафле')
        return


def setup(bot):
    bot.add_cog(Music(bot))
