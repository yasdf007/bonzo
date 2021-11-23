"""
Микс из
https://github.com/PythonistaGuild/Wavelink/blob/master/examples/advanced.py
+
https://github.com/PythonistaGuild/Wavelink/blob/master/examples/playlist.py
+
https://github.com/Carberra/discord.py-music-tutorial/blob/master/bot/cogs/music.py
"""


import asyncio
from os import getenv
import discord
import re
from discord.ext.commands.context import Context
from discord.ext.commands import MissingRequiredArgument, BadArgument
import wavelink
from discord.ext import commands
from discord import Embed
from typing import Union
from datetime import timedelta

from discord_slash import SlashContext, cog_ext
from discord_slash.error import SlashCommandError
from discord_slash.utils.manage_commands import create_choice

from colorama import Fore, Back, Style
from config import guilds
from random import shuffle

from .resources.AutomatedMessages import automata
from .resources.equalizers import equalizers
from .resources.music.bonzoPlayer import BonzoPlayer
from .resources.music.filters import *

RURL = re.compile('https?:\/\/(?:www\.)?.+')
TIME_REGEX = re.compile('([0-9]{1,2})m:([0-9]{1,2})s')


class IncorrectChannelError(commands.CommandError, SlashCommandError):
    pass


class NotInVoice(commands.CommandError, SlashCommandError):
    pass


class QueueTooShort(commands.CommandError, SlashCommandError):
    pass


class NoPrivateMessage(commands.CommandError, SlashCommandError):
    pass


class MusicController:

    def __init__(self, bot, guild_id):
        self.bot = bot
        self.guild_id = guild_id
        self.channel = None

        self.next = asyncio.Event()
        self.queue = asyncio.Queue()

        self.now_playing = None

        self.loop = False
        self.toLoop = None

        self.task = self.bot.loop.create_task(self.controller_loop())

    async def controller_loop(self):
        await self.bot.wait_until_ready()

        player = self.bot.wavelink.get_player(self.guild_id, cls=BonzoPlayer)

        while True:
            if self.now_playing:
                await self.now_playing.delete()

            self.next.clear()

            song = self.toLoop if (self.loop) else (await self.queue.get())

            await player.play(song, replace=False)
            self.now_playing = await self.channel.send(embed=await self.nowPlayingEmbed(player=player))
            await self.next.wait()

    async def stop(self):
        self.task.cancel()

    async def nowPlayingEmbed(self, player):
        track = player.current
        if not track:
            return

        qsize = self.queue.qsize()

        embed = Embed(title=f'Сейчас играет {track.title}')

        embed.set_thumbnail(url=track.thumb)
        embed.add_field(name='Продолжительность', value=str(
            timedelta(milliseconds=int(track.length))))
        embed.add_field(name='Очередь', value=str(qsize))
        embed.add_field(name='Громкость', value=f'**`{player.volume}%`**')
        embed.add_field(name='Ссылка на трек',
                        value=f'[Клик]({track.uri})')

        return embed


class Music(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.controllers = {}
        self.eqs = equalizers
        self.password = getenv('LAVAPASS')
        self.dc_flag = {}

        if not hasattr(bot, 'wavelink'):
            self.bot.wavelink = wavelink.Client(bot=self.bot)

        self.bot.loop.create_task(self.start_nodes())

    async def start_nodes(self):
        await self.bot.wait_until_ready()

        if self.password == None:
            print(f"/\n{Fore.RED}ERROR WHILE CONNECTING TO LAVALINK SERVER \nPASSWORD IS NOT SPECIFIED\nMUSIC UNLOADING... {Style.RESET_ALL}")
            self.bot.unload_extension('commands.music')
            return

        # Initiate our nodes. For this example we will use one server.
        # Region should be a discord.py guild.region e.g sydney or us_central (Though this is not technically required)
        node = await self.bot.wavelink.initiate_node(host='java',
                                                     port=2333,
                                                     rest_uri='http://java:2333',
                                                     password=self.password,
                                                     identifier='TEST',
                                                     region='eu')

        if not node.is_available:
            print(f"/ \n {Fore.RED}ERROR WHILE CONNECTING TO LAVALINK SERVER \nLAVALINK SERVER IS DOWN/NOT RUNNING\nMUSIC UNLOADING... {Style.RESET_ALL}")
            self.bot.unload_extension('commands.music')
            return
        # Set our node hook callback
        node.set_hook(self.on_event_hook)

    async def on_event_hook(self, event):
        """Node hook callback."""
        if isinstance(event, (wavelink.TrackEnd, wavelink.TrackException)):
            controller = self.get_controller(event.player)

            if isinstance(event, wavelink.TrackException):
                await controller.channel.send(f'Ошибка при проигрывании {event.player.current}')

            controller.next.set()

    def get_controller(self, value: Union[commands.Context, wavelink.Player]):
        if isinstance(value, commands.Context):
            gid = value.guild.id
        else:
            gid = value.guild_id

        try:
            controller = self.controllers[gid]
        except KeyError:
            controller = MusicController(self.bot, gid)
            self.controllers[gid] = controller

        return controller

    async def cog_check(self, ctx):
        """A local check which applies to all commands in this cog."""
        if not ctx.guild:
            raise NoPrivateMessage
        return True

    async def cog_command_error(self, ctx, error):
        """A local error handler for all errors arising from commands in this cog."""
        if isinstance(error, NoPrivateMessage):
            try:
                return await ctx.send(embed=automata.generateEmbErr('Эту команду нельзя использовать в ЛС.', error=error))
            except discord.HTTPException:
                pass

        if isinstance(error, IncorrectChannelError):
            return await ctx.send(error)

        if isinstance(error, NotInVoice):
            return await ctx.send(embed=automata.generateEmbErr('Для использования комманды нужно быть в войсе', error=error))

        if isinstance(error, MissingRequiredArgument):
            return await ctx.send(embed=automata.generateEmbErr('Нужно указать запрос', error=error))

        if isinstance(error, QueueTooShort):
            return await ctx.send(embed=automata.generateEmbErr('Очередь слишком маленькая для перемешивания', error=error))

        if isinstance(error, FilterInvalidArgument):
            return await ctx.send(embed=automata.generateEmbErr('Значение должно быть больше нуля', error=error))

        if isinstance(error, BadArgument):
            return await ctx.send(embed=automata.generateEmbErr('Неправильный запрос', error=error))

        raise error

    @commands.Cog.listener()
    async def on_slash_command_error(self, ctx, error):
        if isinstance(error, NoPrivateMessage):
            try:
                return await ctx.send(embed=automata.generateEmbErr('Эту команду нельзя использовать в ЛС.', error=error))
            except discord.HTTPException:
                pass

        if isinstance(error, IncorrectChannelError):
            return await ctx.send(error)

        if isinstance(error, NotInVoice):
            return await ctx.send(embed=automata.generateEmbErr('Для использования комманды нужно быть в войсе', error=error))

        if isinstance(error, MissingRequiredArgument):
            return await ctx.send(embed=automata.generateEmbErr('Нужно указать запрос', error=error))

        if isinstance(error, QueueTooShort):
            return await ctx.send(embed=automata.generateEmbErr('Очередь слишком маленькая для перемешивания', error=error))

        if isinstance(error, FilterInvalidArgument):
            return await ctx.send(embed=automata.generateEmbErr('Значение должно быть больше нуля', error=error))

        if isinstance(error, BadArgument):
            return await ctx.send(embed=automata.generateEmbErr('Неправильный запрос', error=error))

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if member.id == self.bot.user.id:
            player = self.bot.wavelink.get_player(member.guild.id, cls=BonzoPlayer)

            # перемещение бота по каналам
            if (before.channel and after.channel) and before.channel != after.channel:
                # в новом канале нет людей
                if len([user for user in after.channel.members if not user.bot]) < 1:
                    del self.dc_flag[member.guild.id]

                    await self.teardown(member.guild.id)
                    return
                else:
                    # ставится новый канал проигрывания музыки
                    player.channel_id = after.channel.id
                    return

            # дисконнект из войса кнопкой в дискорде
            if not self.dc_flag[member.guild.id] and before.channel and not after.channel:
                del self.dc_flag[member.guild.id]

                await self.teardown(member.guild.id)
                return

        if member.bot:
            return

        if not member.guild.id in self.controllers:
            return

        player = self.bot.wavelink.get_player(member.guild.id, cls=BonzoPlayer)
        if not player.is_connected:
            return
        # Вышел из войса с ботом или поменял канал
        if (before.channel and not after.channel) or ((before.channel and after.channel) and before.channel != after.channel):
            if len([user for user in self.bot.get_channel(player.channel_id).members if not user.bot]) < 1:
                del self.dc_flag[member.guild.id]

                await self.teardown(member.guild.id)

    async def checkIsSameVoice(self, ctx, voiceChannel):
        if ctx.author not in voiceChannel.members:
            raise IncorrectChannelError(automata.generateEmbErr('f{ctx.author}, Вы должен быть подключены к `{voiceChannel.name}` для использования музыкальных команд', error=IncorrectChannelError))

    async def teardown(self, guild_id):
        player = self.bot.wavelink.get_player(guild_id, cls=BonzoPlayer)

        await self.controllers[guild_id].stop()

        del self.controllers[guild_id]

        await player.destroy()

    async def connect(self, ctx, channel: discord.VoiceChannel):
        """Connect to a valid voice channel."""
        if not channel:
            try:
                channel = ctx.author.voice.channel
            except AttributeError:
                raise NotInVoice

        if not isinstance(channel, discord.VoiceChannel):
            raise IncorrectChannelError(automata.generateEmbErr(f'Указанный канал не является голосовым', error=IncorrectChannelError))

        try:
            guild_id = ctx.guild_id
        except AttributeError:
            guild_id = ctx.guild.id

        player = self.bot.wavelink.get_player(guild_id, cls=BonzoPlayer)

        if player.channel_id:
            vc = self.bot.get_channel(player.channel_id)
            await self.checkIsSameVoice(ctx, vc)

        await ctx.send(f'Подрубаюсь в **`{channel.name}`**\nВидео с ограничением по возрасту не будут работать', delete_after=15)
        await player.connect(channel.id)

        controller = self.get_controller(ctx)
        controller.channel = ctx.channel

    @commands.command(name='play', description='Играет музыку по ссылке или по названию')
    async def play_prefix(self, ctx: Context, *query):
        try:
            query = " ".join(query)
            await self.play(ctx, query)
        except:
            raise

    @cog_ext.cog_slash(name='play', description='Играет музыку по ссылке или по названию')
    async def play_slash(self, ctx: SlashContext, query: str):
        if not ctx.guild:
            raise NoPrivateMessage
        try:
            await self.play(ctx, query)
        except:
            raise

    async def play(self, ctx, query: str):
        if len(query) < 1:
            raise MissingRequiredArgument(ctx.author)
        try:
            guild_id = ctx.guild_id
        except AttributeError:
            guild_id = ctx.guild.id

        self.dc_flag[ctx.guild.id] = False

        player = self.bot.wavelink.get_player(guild_id, cls=BonzoPlayer)
        try:
            if player.is_connected:
                vc = self.bot.get_channel(player.channel_id)
                await self.checkIsSameVoice(ctx, vc)
            else:
                await self.connect(ctx, ctx.author.voice.channel)

        except AttributeError:
            raise NotInVoice

        query = query.strip('<>')
        await ctx.send(f'Ищу `{query}`', delete_after=15)

        if not RURL.match(query):
            query = f'ytsearch:{query}'

        tracks = await self.bot.wavelink.get_tracks(f'{query}')

        if not tracks:
            return await ctx.send('Не нашел песню', delete_after=15)

        controller = self.get_controller(ctx)

        embed = Embed(
            title=f'Добавил в очередь')

        if isinstance(tracks, wavelink.TrackPlaylist):
            for track in tracks.tracks:
                track = wavelink.Track(
                    track.id, track.info)

                await controller.queue.put(track)

            embed.description = f'Плейлист {tracks.data["playlistInfo"]["name"]} c {len(tracks.tracks)} треками'
        else:
            track = tracks[0]

            duration = timedelta(milliseconds=int(track.length))

            await controller.queue.put(track)

            embed.set_thumbnail(
                url=track.thumb)

            embed.add_field(
                name='Название', value=f'[{track.title}]({track.uri})')

            embed.add_field(
                name='Автор', value=f'{track.author}')

            embed.add_field(
                name='Продолжительность', value=duration)

            embed.add_field(
                name='Позиция в очереди', value=f'{controller.queue.qsize()}')

        await ctx.send(embed=embed, delete_after=15)

    @commands.command(name='pause', description='Останавливает музыку')
    async def pause_prefix(self, ctx: Context):
        await self.pause(ctx)

    @cog_ext.cog_slash(name='pause', description='Останавливает музыку')
    async def pause_slash(self, ctx: SlashContext):
        if not ctx.guild:
            raise NoPrivateMessage
        await self.pause(ctx)

    async def pause(self, ctx):
        """Pause the player."""
        player = self.bot.wavelink.get_player(ctx.guild.id, cls=BonzoPlayer)

        if not player.is_connected:
            return

        vc = self.bot.get_channel(player.channel_id)
        await self.checkIsSameVoice(ctx, vc)

        if not player.is_playing:
            return await ctx.send('Я ничего не играю', delete_after=15)

        if player.is_paused:
            return await ctx.send('Я на паузе', delete_after=15)

        await ctx.send('Останавливаю проигрывание', delete_after=15)
        await player.set_pause(True)

    @commands.command(name='resume', description='Возобновляет музыку')
    async def resume_prefix(self, ctx: Context):
        await self.resume(ctx)

    @cog_ext.cog_slash(name='resume', description='Возобновляет музыку')
    async def resume_slash(self, ctx: SlashContext):
        if not ctx.guild:
            raise NoPrivateMessage
        await self.resume(ctx)

    async def resume(self, ctx):
        """Resume the player from a paused state."""
        player = self.bot.wavelink.get_player(ctx.guild.id, cls=BonzoPlayer)

        if not player.is_connected:
            return

        vc = self.bot.get_channel(player.channel_id)
        await self.checkIsSameVoice(ctx, vc)

        if not player.is_playing:
            return await ctx.send('Я ничего не играю', delete_after=15)

        if not player.paused:
            return await ctx.send('Я не в паузе', delete_after=15)

        await ctx.send('Возобновляю проигрывание', delete_after=15)
        await player.set_pause(False)

    @commands.command(name='skip', description='Пропускает играющую музыку')
    async def skip_prefix(self, ctx: Context):
        await self.skip(ctx)

    @cog_ext.cog_slash(name='skip', description='Пропускает играющую музыку')
    async def skip_slash(self, ctx: SlashContext):
        if not ctx.guild:
            raise NoPrivateMessage
        await self.skip(ctx)

    async def skip(self, ctx):
        """Skip the currently playing song."""
        player = self.bot.wavelink.get_player(ctx.guild.id, cls=BonzoPlayer)

        if not player.is_connected:
            return

        vc = self.bot.get_channel(player.channel_id)
        await self.checkIsSameVoice(ctx, vc)

        if not player.is_playing:
            return await ctx.send('Я ничего не играю', delete_after=15)

        embed = Embed(
            title=f'Скипнул `{player.current.title}`')

        controller = self.get_controller(ctx)
        controller.loop = False

        await ctx.send(embed=embed, delete_after=15)
        await player.stop()

    @commands.command(name='volume', description='Устанавливает громкость плеера', aliases=['vol'])
    async def volume_prefix(self, ctx: Context, vol: int):
        await self.volume(ctx, vol)

    @cog_ext.cog_slash(name='volume', description='Устанавливает громкость плеера')
    async def volume_slash(self, ctx: SlashContext, vol: int):
        if not ctx.guild:
            raise NoPrivateMessage
        await self.volume(ctx, vol)

    async def volume(self, ctx, vol: int):
        """Set the player volume."""
        player = self.bot.wavelink.get_player(ctx.guild.id, cls=BonzoPlayer)

        if not player.is_connected:
            return

        vc = self.bot.get_channel(player.channel_id)
        await self.checkIsSameVoice(ctx, vc)

        if not player.is_playing:
            return await ctx.send('Я ничего не играю', delete_after=15)

        vol = max(min(vol, 1000), 0)

        embed = Embed(
            title=f':speaker: Установил громкость плеера `{vol}`')
        await ctx.send(embed=embed, delete_after=15)

        await player.set_volume(vol)

    @commands.command(name='now_playing', description='Показывает текущий трек', aliases=['np', 'current', 'nowplaying'])
    async def now_playing_prefix(self, ctx: Context):
        await self.now_playing(ctx)

    @cog_ext.cog_slash(name='now_playing', description='Показывает текущий трек')
    async def now_playing_slash(self, ctx: SlashContext):
        if not ctx.guild:
            raise NoPrivateMessage
        await self.now_playing(ctx)

    async def now_playing(self, ctx):
        """Retrieve the currently playing song."""
        player = self.bot.wavelink.get_player(ctx.guild.id, cls=BonzoPlayer)

        if not player.is_connected:
            return

        vc = self.bot.get_channel(player.channel_id)
        await self.checkIsSameVoice(ctx, vc)

        if not player.current:
            return await ctx.send('Я ничего не играю', delete_after=15)

        controller = self.get_controller(ctx)
        await controller.now_playing.delete()

        controller.now_playing = await ctx.send(embed=await controller.nowPlayingEmbed(player))

    @commands.command(name='queue', description='Показывает очередь из треков (первые 5)', aliases=['q'])
    async def queue_prefix(self, ctx: Context):
        await self.queue(ctx)

    @cog_ext.cog_slash(name='queue', description='Показывает очередь из треков (первые 5)')
    async def queue_slash(self, ctx: SlashContext):
        if not ctx.guild:
            raise NoPrivateMessage
        await self.queue(ctx)

    async def queue(self, ctx):
        """Retrieve information on the next 5 songs from the queue."""
        player = self.bot.wavelink.get_player(ctx.guild.id, cls=BonzoPlayer)
        if not player.is_connected:
            return

        vc = self.bot.get_channel(player.channel_id)
        await self.checkIsSameVoice(ctx, vc)

        controller = self.get_controller(ctx)

        if not player.current or not controller.queue._queue:
            return await ctx.send('Очередь пустая', delete_after=15)

        upcoming = list(controller.queue._queue)

        embed = discord.Embed(
            title=f'В очереди - {len(upcoming)} (первые 5)')

        for song in upcoming[:5]:
            embed.add_field(name=song.author,
                            value=f'[{song.title}]({song.uri})', inline=False)
        await ctx.send(embed=embed, delete_after=15)

    @commands.command(name='stop', description='Отключается и чистит очередь', aliases=['disconnect', 'dc'])
    async def stop_prefix(self, ctx: Context):
        await self.stop(ctx)

    @cog_ext.cog_slash(name='stop', description='Отключается и чистит очередь')
    async def stop_slash(self, ctx: SlashContext):
        if not ctx.guild:
            raise NoPrivateMessage
        await self.stop(ctx)

    async def stop(self, ctx):
        """Stop and disconnect the player and controller."""
        player = self.bot.wavelink.get_player(ctx.guild.id, cls=BonzoPlayer)

        if not player.is_connected:
            return await ctx.send('Я не в войсе', delete_after=15)

        vc = self.bot.get_channel(player.channel_id)
        await self.checkIsSameVoice(ctx, vc)

        self.dc_flag[ctx.guild.id] = True
        await self.teardown(ctx.guild.id)

        await ctx.send('Отключился и удалил очередь', delete_after=15)

    @commands.command(name='equalizer', description='Пресеты эквалайзера музыки', aliases=['eq'])
    async def equalizer_prefix(self, ctx: Context, equalizer='None'):
        await self.equalizer(ctx, equalizer)

    @cog_ext.cog_slash(name='equalizer', description='Пресеты эквалайзера музыки',
                       options=[
                           {
                               "name": "equalizer",
                               "description": "Пресеты эквалайзера музыки",
                               "type": 3,
                               "required": "true",
                               "choices": [
                                   create_choice(
                                       name="bass",
                                       value="bass"
                                   ),
                                   create_choice(
                                       name="default",
                                       value="default"
                                   ),
                               ]
                           }
                       ]
                       )
    async def equalizer_slash(self, ctx: SlashContext, equalizer='None'):
        if not ctx.guild:
            raise NoPrivateMessage
        await self.equalizer(ctx, equalizer)

    async def equalizer(self, ctx, equalizer='None'):
        """Change the players equalizer."""
        player = self.bot.wavelink.get_player(ctx.guild.id, cls=BonzoPlayer)

        if not player.is_connected:
            return await ctx.send('Я не в войсе', delete_after=15)

        vc = self.bot.get_channel(player.channel_id)
        await self.checkIsSameVoice(ctx, vc)

        if not player.is_playing:
            return await ctx.send('Я ничего не играю', delete_after=15)

        eq = self.eqs.get(equalizer.lower(), None)

        if not eq or not equalizer:
            joined = ", ".join(self.eqs.keys())
            return await ctx.send(f'Такого эквалайзера нет, доступны: {joined}', delete_after=15)

        await player.set_eq(eq)
        await ctx.send(f'Поставил эквалайзер {equalizer}. Применение займет несколько секунд...', delete_after=15)

    @commands.command(name='loop', description='Зацикливает, расцикливает трек')
    async def loop_prefix(self, ctx: Context):
        await self.loop(ctx)

    @cog_ext.cog_slash(name='loop', description='Зацикливает, расцикливает трек')
    async def loop_slash(self, ctx: SlashContext):
        if not ctx.guild:
            raise NoPrivateMessage
        await self.loop(ctx)

    async def loop(self, ctx):
        """Stop and disconnect the player and controller."""
        player = self.bot.wavelink.get_player(ctx.guild.id, cls=BonzoPlayer)

        if not player.is_connected:
            return

        vc = self.bot.get_channel(player.channel_id)
        await self.checkIsSameVoice(ctx, vc)

        if not player.is_playing:
            return await ctx.send('Я ничего не играю', delete_after=15)

        controller = self.get_controller(ctx)

        if controller.loop == False:
            embed = Embed(title=f'Трек `{player.current}` зациклен')
            controller.loop = True
            controller.toLoop = player.current
        else:
            embed = Embed(title=f'Трек `{player.current}` больше не зациклен')
            controller.loop = False
            controller.toLoop = None

        await ctx.send(embed=embed, delete_after=15)

    @commands.command(name='shuffle', description='Перемешивает треки в очереди', aliases=['mix'])
    async def shuffle_prefix(self, ctx: Context):
        await self.shuffle_(ctx)

    @cog_ext.cog_slash(name='shuffle', description='Перемешивает треки в очереди')
    async def shuffle_slash(self, ctx: SlashContext):
        if not ctx.guild:
            raise NoPrivateMessage
        await self.shuffle_(ctx)

    async def shuffle_(self, ctx):
        """Stop and disconnect the player and controller."""
        player = self.bot.wavelink.get_player(ctx.guild.id, cls=BonzoPlayer)

        if not player.is_connected:
            return

        vc = self.bot.get_channel(player.channel_id)
        await self.checkIsSameVoice(ctx, vc)

        controller = self.get_controller(ctx)

        if not (len(controller.queue._queue) > 2):
            raise QueueTooShort

        shuffle(controller.queue._queue)
        return await ctx.send('Очередь перемешана', delete_after=15)

    @commands.command(name='skip_to', description='Пропускает до таймкода в треке (формат 0m:00s)', aliases=['seek'])
    async def skip_to_prefix(self, ctx: Context, time: str):
        await self.skip_to(ctx, time)

    @cog_ext.cog_slash(name='skip_to', description='Пропускает до таймкода в треке (формат 0m:00s)')
    async def skip_to_slash(self, ctx: SlashContext, time: str):
        if not ctx.guild:
            raise NoPrivateMessage
        await self.skip_to(ctx, time)

    async def skip_to(self, ctx, time: str):
        player = self.bot.wavelink.get_player(ctx.guild.id, cls=BonzoPlayer)

        if not player.is_connected:
            return

        vc = self.bot.get_channel(player.channel_id)
        await self.checkIsSameVoice(ctx, vc)

        if not player.is_playing:
            return await ctx.send('Я ничего не играю', delete_after=15)

        match = TIME_REGEX.match(time)
        if not match:
            return await ctx.send('Неправильный формат времени', delete_after=15)

        milliseconds = (int(match.group(1)) * 60 + int(match.group(2))) * 1000

        await player.seek(milliseconds)

        await ctx.send(f'Скипаю до {time}', delete_after=15)

    @commands.command(name='speed', description='Ставит скорость проигрывания')
    async def set_speed_prefix(self, ctx: Context, speed: float):
        await self.set_speed(ctx, speed)

    @cog_ext.cog_slash(name='speed', description='Ставит скорость проигрывания')
    async def set_speed_slash(self, ctx: SlashContext, speed: float):
        if not ctx.guild:
            raise NoPrivateMessage
        await self.set_speed(ctx, speed)

    async def set_speed(self, ctx: Context, speed: float):
        if speed <= 0:
            raise FilterInvalidArgument

        player = self.bot.wavelink.get_player(ctx.guild.id, cls=BonzoPlayer)

        if not player.is_connected:
            return

        vc = self.bot.get_channel(player.channel_id)
        await self.checkIsSameVoice(ctx, vc)

        if not player.is_playing:
            return await ctx.send('Я ничего не играю', delete_after=15)

        await player.set_speed(speed)

        await ctx.send(f'Поставил скорость {speed}. Применение займет несколько секунд...', delete_after=15)

    @commands.command(name='pitch', description='Ставит высоту проигрывания')
    async def set_pitch_prefix(self, ctx: Context, pitch: float):
        await self.set_pitch(ctx, pitch)

    @cog_ext.cog_slash(name='pitch', description='Ставит высоту проигрывания')
    async def set_pitch_slash(self, ctx: SlashContext, pitch: float):
        if not ctx.guild:
            raise NoPrivateMessage
        await self.set_pitch(ctx, pitch)

    async def set_pitch(self, ctx: Context, pitch: float):
        if pitch <= 0:
            raise FilterInvalidArgument

        player = self.bot.wavelink.get_player(ctx.guild.id, cls=BonzoPlayer)

        if not player.is_connected:
            return

        vc = self.bot.get_channel(player.channel_id)
        await self.checkIsSameVoice(ctx, vc)

        if not player.is_playing:
            return await ctx.send('Я ничего не играю', delete_after=15)

        await player.set_pitch(pitch)

        await ctx.send(f'Поставил высоту {pitch}. Применение займет несколько секунд...', delete_after=15)

    @commands.command(name='reset_filters', description='Убирает фильтры')
    async def reset_filters_prefix(self, ctx: Context, pitch: float):
        await self.reset_filters(ctx, pitch)

    @cog_ext.cog_slash(name='reset_filters', description='Убирает фильтры')
    async def reset_filters_slash(self, ctx: SlashContext, pitch: float):
        if not ctx.guild:
            raise NoPrivateMessage
        await self.reset_filters(ctx, pitch)

    async def reset_filters(self, ctx: Context):
        player = self.bot.wavelink.get_player(ctx.guild.id, cls=BonzoPlayer)

        if not player.is_connected:
            return

        vc = self.bot.get_channel(player.channel_id)
        await self.checkIsSameVoice(ctx, vc)

        if not player.is_playing:
            return await ctx.send('Я ничего не играю', delete_after=15)

        await player.reset_filter()

        await ctx.send(f'Убрал фильтры. Применение займет несколько секунд...', delete_after=15)


def setup(bot):
    bot.add_cog(Music(bot))
