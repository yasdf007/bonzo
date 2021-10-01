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

        self.bot.loop.create_task(self.controller_loop())

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

        if not hasattr(bot, 'wavelink'):
            self.bot.wavelink = wavelink.Client(bot=self.bot)

        self.bot.loop.create_task(self.start_nodes())

    async def start_nodes(self):
        await self.bot.wait_until_ready()
        try:
            if getenv('LAVAPASS') == None:
                raise NameError("No password Specified")
            password = getenv('LAVAPASS')
        except:
            print(f'/ \n {Fore.GREEN} Music: {Style.RESET_ALL} {Fore.RED} NO LAVALINK NODE PASSWORD SPECIFIED. MUSIC UNLOADING. {Style.RESET_ALL} \n /')
            self.cog_unload()
        # Initiate our nodes. For this example we will use one server.
        # Region should be a discord.py guild.region e.g sydney or us_central (Though this is not technically required)
        node = await self.bot.wavelink.initiate_node(host='java',
                                                     port=2333,
                                                     rest_uri='http://java:2333',
                                                     password=password,
                                                     identifier='TEST',
                                                     region='eu')

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
            raise commands.NoPrivateMessage
        return True

    async def cog_command_error(self, ctx, error):
        """A local error handler for all errors arising from commands in this cog."""
        if isinstance(error, commands.NoPrivateMessage):
            try:
                return await ctx.send('This command can not be used in Private Messages.')
            except discord.HTTPException:
                pass

        if isinstance(error, IncorrectChannelError):
            return await ctx.send(error)

        if isinstance(error, NotInVoice):
            return await ctx.send('Ты не в войсе')

        if isinstance(error, MissingRequiredArgument):
            return await ctx.send('Нужно указать запрос')

        if isinstance(error, QueueTooShort):
            return await ctx.send('Очередь слишком маленькая для перемешивания')

        if isinstance(error, FilterInvalidArgument):
            return await ctx.send('Значение должно быть больше нуля')

        if isinstance(error, BadArgument):
            return await ctx.send('Неправильный запрос')

        raise error

    @commands.Cog.listener()
    async def on_slash_command_error(self, ctx, error):
        if isinstance(error, commands.NoPrivateMessage):
            try:
                return await ctx.send('This command can not be used in Private Messages.')
            except discord.HTTPException:
                pass

        if isinstance(error, IncorrectChannelError):
            return await ctx.send(str(error))

        if isinstance(error, NotInVoice):
            return await ctx.send('Ты не в войсе')

        if isinstance(error, MissingRequiredArgument):
            return await ctx.send('Нужно указать запрос')

        if isinstance(error, QueueTooShort):
            return await ctx.send('Очередь слишком маленькая для перемешивания')

        if isinstance(error, FilterInvalidArgument):
            return await ctx.send('Значение должно быть больше нуля')

        if isinstance(error, BadArgument):
            return await ctx.send('Неправильный запрос')

        raise error

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if member.bot:
            return

        # Вырубается из войса, если не осталось людей

        # Вышел из войса с ботом или поменял канал
        if (before.channel and not after.channel) or ((before.channel and after.channel) and before.channel != after.channel):
            if len([user for user in before.channel.members if not user.bot]) < 1:
                player = self.bot.wavelink.get_player(
                    member.guild.id, cls=BonzoPlayer)

                try:
                    del self.controllers[member.guild.id]
                except:
                    pass
                await player.destroy()

    async def checkIsSameVoice(self, ctx, voiceChannel):
        if ctx.author not in voiceChannel.members:
            raise IncorrectChannelError(
                f'{ctx.author}, ты должен быть в `{voiceChannel.name}` для использования музыки')

    @commands.command(name='connect', description='Подрубается к войсу')
    async def connect_prefix(self, ctx: Context,  channel: discord.VoiceChannel = None):
        try:
            await self.connect(ctx, channel)
        except:
            raise

    @cog_ext.cog_slash(name='connect', description='Подрубается к войсу')
    async def connect_slash(self, ctx: SlashContext, channel: discord.VoiceChannel = None):
        try:
            await self.connect(ctx, channel)
        except:
            raise

    async def connect(self, ctx, channel: discord.VoiceChannel = None):
        """Connect to a valid voice channel."""
        if not channel:
            try:
                channel = ctx.author.voice.channel
            except AttributeError:
                raise NotInVoice
        try:
            guild_id = ctx.guild_id
        except AttributeError:
            guild_id = ctx.guild.id

        player = self.bot.wavelink.get_player(guild_id, cls=BonzoPlayer)

        if player.channel_id:
            vc = self.bot.get_channel(player.channel_id)
            await self.checkIsSameVoice(ctx, vc)

        await ctx.send(f'Подрубаюсь в **`{channel.name}`**\nВидео с ограничением по возрасту не будут работать')
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

        player = self.bot.wavelink.get_player(guild_id, cls=BonzoPlayer)
        try:
            if player.is_connected:
                vc = self.bot.get_channel(player.channel_id)
                await self.checkIsSameVoice(ctx, vc)
            else:
                if isinstance(ctx, Context):
                    await ctx.invoke(self.connect_prefix)
                if isinstance(ctx, SlashContext):
                    await ctx.invoke(self.connect_slash, ctx, ctx.author.voice.channel)
        except AttributeError:
            raise NotInVoice

        query = query.strip('<>')
        await ctx.send(f'Ищу `{query}`')

        if not RURL.match(query):
            query = f'ytsearch:{query}'

        tracks = await self.bot.wavelink.get_tracks(f'{query}')

        if not tracks:
            return await ctx.send('Не нашел песню')

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

        await ctx.send(embed=embed)

    @commands.command(name='pause', description='Останавливает музыку')
    async def pause_prefix(self, ctx: Context):
        await self.pause(ctx)

    @cog_ext.cog_slash(name='pause', description='Останавливает музыку')
    async def pause_slash(self, ctx: SlashContext):
        await self.pause(ctx)

    async def pause(self, ctx):
        """Pause the player."""
        player = self.bot.wavelink.get_player(ctx.guild.id, cls=BonzoPlayer)

        if not player.is_connected:
            return

        vc = self.bot.get_channel(player.channel_id)
        await self.checkIsSameVoice(ctx, vc)

        if not player.is_playing:
            return await ctx.send('Я ничего не играю')

        if player.is_paused:
            return await ctx.send('Я на паузе')

        await ctx.send('Останавливаю проигрывание')
        await player.set_pause(True)

    @commands.command(name='resume', description='Возобновляет музыку')
    async def resume_prefix(self, ctx: Context):
        await self.resume(ctx)

    @cog_ext.cog_slash(name='resume', description='Возобновляет музыку')
    async def resume_slash(self, ctx: SlashContext):
        await self.resume(ctx)

    async def resume(self, ctx):
        """Resume the player from a paused state."""
        player = self.bot.wavelink.get_player(ctx.guild.id, cls=BonzoPlayer)

        if not player.is_connected:
            return

        vc = self.bot.get_channel(player.channel_id)
        await self.checkIsSameVoice(ctx, vc)

        if not player.is_playing:
            return await ctx.send('Я ничего не играю')

        if not player.paused:
            return await ctx.send('Я не в паузе')

        await ctx.send('Возобновляю проигрывание')
        await player.set_pause(False)

    @commands.command(name='skip', description='Пропускает играющую музыку')
    async def skip_prefix(self, ctx: Context):
        await self.skip(ctx)

    @cog_ext.cog_slash(name='skip', description='Пропускает играющую музыку')
    async def skip_slash(self, ctx: SlashContext):
        await self.skip(ctx)

    async def skip(self, ctx):
        """Skip the currently playing song."""
        player = self.bot.wavelink.get_player(ctx.guild.id, cls=BonzoPlayer)

        if not player.is_connected:
            return

        vc = self.bot.get_channel(player.channel_id)
        await self.checkIsSameVoice(ctx, vc)

        if not player.is_playing:
            return await ctx.send('Я ничего не играю')

        embed = Embed(
            title=f'Скипнул `{player.current.title}`')

        controller = self.get_controller(ctx)
        controller.loop = False

        await ctx.send(embed=embed)
        await player.stop()

    @commands.command(name='volume', description='Устанавливает громкость плеера', aliases=['vol'])
    async def volume_prefix(self, ctx: Context, vol: int):
        await self.volume(ctx, vol)

    @cog_ext.cog_slash(name='volume', description='Устанавливает громкость плеера')
    async def volume_slash(self, ctx: SlashContext, vol: int):
        await self.volume(ctx, vol)

    async def volume(self, ctx, vol: int):
        """Set the player volume."""
        player = self.bot.wavelink.get_player(ctx.guild.id, cls=BonzoPlayer)

        if not player.is_connected:
            return

        vc = self.bot.get_channel(player.channel_id)
        await self.checkIsSameVoice(ctx, vc)

        if not player.is_playing:
            return await ctx.send('Я ничего не играю')

        vol = max(min(vol, 1000), 0)

        embed = Embed(
            title=f':speaker: Установил громкость плеера `{vol}`')
        await ctx.send(embed=embed)

        await player.set_volume(vol)

    @commands.command(name='now_playing', description='Показывает текущий трек', aliases=['np', 'current', 'nowplaying'])
    async def now_playing_prefix(self, ctx: Context):
        await self.now_playing(ctx)

    @cog_ext.cog_slash(name='now_playing', description='Показывает текущий трек')
    async def now_playing_slash(self, ctx: SlashContext):
        await self.now_playing(ctx)

    async def now_playing(self, ctx):
        """Retrieve the currently playing song."""
        player = self.bot.wavelink.get_player(ctx.guild.id, cls=BonzoPlayer)

        if not player.is_connected:
            return

        vc = self.bot.get_channel(player.channel_id)
        await self.checkIsSameVoice(ctx, vc)

        if not player.current:
            return await ctx.send('Я ничего не играю')

        controller = self.get_controller(ctx)
        await controller.now_playing.delete()

        controller.now_playing = await ctx.send(embed=await controller.nowPlayingEmbed(player))

    @commands.command(name='queue', description='Показывает очередь из треков (первые 5)', aliases=['q'])
    async def queue_prefix(self, ctx: Context):
        await self.queue(ctx)

    @cog_ext.cog_slash(name='queue', description='Показывает очередь из треков (первые 5)')
    async def queue_slash(self, ctx: SlashContext):
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
            return await ctx.send('Очередь пустая')

        upcoming = list(controller.queue._queue)

        embed = discord.Embed(
            title=f'В очереди - {len(upcoming)} (первые 5)')

        for song in upcoming[:5]:
            embed.add_field(name=song.author,
                            value=f'[{song.title}]({song.uri})', inline=False)
        await ctx.send(embed=embed)

    @commands.command(name='stop', description='Отключается и чистит очередь', aliases=['disconnect', 'dc'])
    async def stop_prefix(self, ctx: Context):
        await self.stop(ctx)

    @cog_ext.cog_slash(name='stop', description='Отключается и чистит очередь')
    async def stop_slash(self, ctx: SlashContext):
        await self.stop(ctx)

    async def stop(self, ctx):
        """Stop and disconnect the player and controller."""
        player = self.bot.wavelink.get_player(ctx.guild.id, cls=BonzoPlayer)

        if not player.is_connected:
            return

        vc = self.bot.get_channel(player.channel_id)
        await self.checkIsSameVoice(ctx, vc)

        try:
            del self.controllers[ctx.guild.id]
        except KeyError:
            await player.destroy()
            return await ctx.send('Отключился и удалил очередь')

        await player.destroy()
        await ctx.send('Отключился и удалил очередь')

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
        await self.equalizer(ctx, equalizer)

    async def equalizer(self, ctx, equalizer='None'):
        """Change the players equalizer."""
        player = self.bot.wavelink.get_player(ctx.guild.id, cls=BonzoPlayer)

        if not player.is_connected:
            return

        vc = self.bot.get_channel(player.channel_id)
        await self.checkIsSameVoice(ctx, vc)

        if not player.is_playing:
            return await ctx.send('Я ничего не играю')

        eq = self.eqs.get(equalizer.lower(), None)

        if not eq or not equalizer:
            joined = ", ".join(self.eqs.keys())
            return await ctx.send(f'Такого эквалайзера нет, доступны: {joined}')

        await player.set_eq(eq)
        await ctx.send(f'Поставил эквалайзер {equalizer}. Применение займет несколько секунд...')

    @commands.command(name='loop', description='Зацикливает, расцикливает трек')
    async def loop_prefix(self, ctx: Context):
        await self.loop(ctx)

    @cog_ext.cog_slash(name='loop', description='Зацикливает, расцикливает трек')
    async def loop_slash(self, ctx: SlashContext):
        await self.loop(ctx)

    async def loop(self, ctx):
        """Stop and disconnect the player and controller."""
        player = self.bot.wavelink.get_player(ctx.guild.id, cls=BonzoPlayer)

        if not player.is_connected:
            return

        vc = self.bot.get_channel(player.channel_id)
        await self.checkIsSameVoice(ctx, vc)

        if not player.is_playing:
            return await ctx.send('Я ничего не играю')

        controller = self.get_controller(ctx)

        if controller.loop == False:
            embed = Embed(title=f'Трек `{player.current}` зациклен')
            controller.loop = True
            controller.toLoop = player.current
        else:
            embed = Embed(title=f'Трек `{player.current}` больше не зациклен')
            controller.loop = False
            controller.toLoop = None

        await ctx.send(embed=embed)

    @commands.command(name='shuffle', description='Перемешивает треки в очереди', aliases=['mix'])
    async def shuffle_prefix(self, ctx: Context):
        await self.shuffle_(ctx)

    @cog_ext.cog_slash(name='shuffle', description='Перемешивает треки в очереди')
    async def shuffle_slash(self, ctx: SlashContext):
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
        return await ctx.send('Очередь перемешана')

    @commands.command(name='skip_to', description='Пропускает до таймкода в треке (формат 0m:00s)', aliases=['seek'])
    async def skip_to_prefix(self, ctx: Context, time: str):
        await self.skip_to(ctx, time)

    @cog_ext.cog_slash(name='skip_to', description='Пропускает до таймкода в треке (формат 0m:00s)')
    async def skip_to_slash(self, ctx: SlashContext, time: str):
        await self.skip_to(ctx, time)

    async def skip_to(self, ctx, time: str):
        player = self.bot.wavelink.get_player(ctx.guild.id, cls=BonzoPlayer)

        if not player.is_connected:
            return

        vc = self.bot.get_channel(player.channel_id)
        await self.checkIsSameVoice(ctx, vc)

        if not player.is_playing:
            return await ctx.send('Я ничего не играю')

        match = TIME_REGEX.match(time)
        if not match:
            return await ctx.send('Неправильный формат времени')

        milliseconds = (int(match.group(1)) * 60 + int(match.group(2))) * 1000

        await player.seek(milliseconds)

        await ctx.send(f'Скипаю до {time}')

    @commands.command(name='speed', description='Ставит скорость проигрывания')
    async def set_speed_prefix(self, ctx: Context, speed: float):
        await self.set_speed(ctx, speed)

    @cog_ext.cog_slash(name='speed', description='Ставит скорость проигрывания')
    async def set_speed_slash(self, ctx: SlashContext, speed: float):
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
            return await ctx.send('Я ничего не играю')

        await player.set_speed(speed)

        await ctx.send(f'Поставил скорость {speed}. Применение займет несколько секунд...')

    @commands.command(name='pitch', description='Ставит высоту проигрывания')
    async def set_pitch_prefix(self, ctx: Context, pitch: float):
        await self.set_pitch(ctx, pitch)

    @cog_ext.cog_slash(name='pitch', description='Ставит высоту проигрывания')
    async def set_pitch_slash(self, ctx: SlashContext, pitch: float):
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
            return await ctx.send('Я ничего не играю')

        await player.set_pitch(pitch)

        await ctx.send(f'Поставил высоту {pitch}. Применение займет несколько секунд...')

    @commands.command(name='reset_filters', description='Убирает фильтры')
    async def reset_filters_prefix(self, ctx: Context, pitch: float):
        await self.reset_filters(ctx, pitch)

    @cog_ext.cog_slash(name='reset_filters', description='Убирает фильтры')
    async def reset_filters_slash(self, ctx: SlashContext, pitch: float):
        await self.reset_filters(ctx, pitch)

    async def reset_filters(self, ctx: Context):
        player = self.bot.wavelink.get_player(ctx.guild.id, cls=BonzoPlayer)

        if not player.is_connected:
            return

        vc = self.bot.get_channel(player.channel_id)
        await self.checkIsSameVoice(ctx, vc)

        if not player.is_playing:
            return await ctx.send('Я ничего не играю')

        await player.reset_filter()

        await ctx.send(f'Убрал фильтры. Применение займет несколько секунд...')


def setup(bot):
    bot.add_cog(Music(bot))
