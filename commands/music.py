"""
Микс из 
https://github.com/PythonistaGuild/Wavelink/blob/master/examples/advanced.py
+
https://github.com/PythonistaGuild/Wavelink/blob/master/examples/playlist.py

"""


import asyncio
from os import getenv
import discord
import re
import wavelink
from discord.ext import commands
from discord import Embed
from typing import Union
from datetime import timedelta
RURL = re.compile('https?:\/\/(?:www\.)?.+')


class IncorrectChannelError(commands.CommandError):
    pass


class NotInVoice(commands.CommandError):
    pass


class MusicController:

    def __init__(self, bot, guild_id):
        self.bot = bot
        self.guild_id = guild_id
        self.channel = None

        self.next = asyncio.Event()
        self.queue = asyncio.Queue()

        self.now_playing = None

        self.bot.loop.create_task(self.controller_loop())

    async def controller_loop(self):
        await self.bot.wait_until_ready()

        player = self.bot.wavelink.get_player(self.guild_id)

        while True:
            if self.now_playing:
                await self.now_playing.delete()

            self.next.clear()

            song = await self.queue.get()
            await player.play(song, replace=False)
            self.now_playing = await self.channel.send(f'Сейчас играет: `{song.author} - {song.title}`')
            await self.next.wait()


class Music(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.controllers = {}

        if not hasattr(bot, 'wavelink'):
            self.bot.wavelink = wavelink.Client(bot=self.bot)

        self.bot.loop.create_task(self.start_nodes())

    async def start_nodes(self):
        await self.bot.wait_until_ready()
        password = getenv('LAVAPASS')
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

    async def cog_before_invoke(self, ctx: commands.Context):
        """Coroutine called before command invocation.
        We mainly just want to check whether the user is in the players controller channel.
        """
        player = self.bot.wavelink.get_player(ctx.guild.id)

        if not player.channel_id:
            return

        channel = self.bot.get_channel(player.channel_id)

        if player.is_connected:
            if ctx.author not in channel.members:
                await ctx.send(f'{ctx.author.mention}, ты должен быть в `{channel.name}` для использования музыки')
                raise IncorrectChannelError

    async def cog_command_error(self, ctx, error):
        """A local error handler for all errors arising from commands in this cog."""
        if isinstance(error, commands.NoPrivateMessage):
            try:
                return await ctx.send('This command can not be used in Private Messages.')
            except discord.HTTPException:
                pass

        if isinstance(error, IncorrectChannelError):
            return

        if isinstance(error, NotInVoice):
            return await ctx.send('Ты не в войсе')

    @commands.command(name='connect')
    async def connect_(self, ctx, *, channel: discord.VoiceChannel = None):
        """Connect to a valid voice channel."""
        if not channel:
            try:
                channel = ctx.author.voice.channel
            except AttributeError:
                raise NotInVoice

        player = self.bot.wavelink.get_player(ctx.guild.id)
        await ctx.send(f'Подрубаюсь в **`{channel.name}`**\nВидео с ограничением по возрасту не будут работать')
        await player.connect(channel.id)

        controller = self.get_controller(ctx)
        controller.channel = ctx.channel

    @commands.command(name='play')
    async def play(self, ctx, *, query: str):
        player = self.bot.wavelink.get_player(ctx.guild.id)
        if not player.is_connected:
            await ctx.invoke(self.connect_)

        await ctx.send(f'Ищу `{query}`')
        """Search for and add a song to the Queue."""
        if not RURL.match(query):
            query = f'ytsearch:{query}'

        tracks = await self.bot.wavelink.get_tracks(f'{query}')

        if not tracks:
            return await ctx.send('Не нашел песню')

        track = tracks[0]

        duration = timedelta(milliseconds=int(track.length))

        controller = self.get_controller(ctx)
        await controller.queue.put(track)

        embed = Embed(
            title=f'Добавил в очередь')

        embed.set_thumbnail(
            url=track.thumb)

        embed.add_field(
            name='Название', value=f'[{track.author} - {track.title}]({track.uri})')

        embed.add_field(
            name='Продолжительность', value=duration)

        embed.add_field(
            name='Позиция в очереди', value=f'{controller.queue.qsize()}')

        await ctx.send(embed=embed)

    @commands.command()
    async def pause(self, ctx):
        """Pause the player."""
        player = self.bot.wavelink.get_player(ctx.guild.id)
        if not player.is_playing:
            return await ctx.send('Я ничего не играю')

        await ctx.send('Останавливаю проигрывание')
        await player.set_pause(True)

    @commands.command()
    async def resume(self, ctx):
        """Resume the player from a paused state."""
        player = self.bot.wavelink.get_player(ctx.guild.id)
        if not player.paused:
            return await ctx.send('Я ничего не играю')

        await ctx.send('Возобновляю проигрывание')
        await player.set_pause(False)

    @commands.command()
    async def skip(self, ctx):
        """Skip the currently playing song."""
        player = self.bot.wavelink.get_player(ctx.guild.id)

        if not player.is_playing:
            return await ctx.send('Я ничего не играю')

        embed = Embed(
            title=f'Скипнул `{player.current.author} - {player.current.title}`')

        await ctx.send(embed=embed)
        await player.stop()

    @commands.command()
    async def volume(self, ctx, *, vol: int):
        """Set the player volume."""
        player = self.bot.wavelink.get_player(ctx.guild.id)
        controller = self.get_controller(ctx)

        vol = max(min(vol, 1000), 0)
        controller.volume = vol

        embed = Embed(
            title=f':speaker: Установил громкость плеера `{vol}`')
        await ctx.send(embed=embed)

        await player.set_volume(vol)

    @commands.command(aliases=['np', 'current', 'nowplaying'])
    async def now_playing(self, ctx):
        """Retrieve the currently playing song."""
        player = self.bot.wavelink.get_player(ctx.guild.id)

        if not player.current:
            return await ctx.send('Я ничего не играю')

        controller = self.get_controller(ctx)
        await controller.now_playing.delete()

        controller.now_playing = await ctx.send(f'Сейчас играет: `{player.current.author} - {player.current.title}`')

    @commands.command(aliases=['q'])
    async def queue(self, ctx):
        """Retrieve information on the next 5 songs from the queue."""
        player = self.bot.wavelink.get_player(ctx.guild.id)
        controller = self.get_controller(ctx)

        if not player.current or not controller.queue._queue:
            return await ctx.send('Очередь пустая')

        upcoming = list(controller.queue._queue)

        fmt = '\n'.join(
            f'`[{song.author} - {song.title}]({song.uri})`' for song in upcoming[:5])

        embed = discord.Embed(
            title=f'В очереди - {len(upcoming)}', description=fmt)

        await ctx.send(embed=embed)

    @commands.command(aliases=['disconnect', 'dc'])
    async def stop(self, ctx):
        """Stop and disconnect the player and controller."""
        player = self.bot.wavelink.get_player(ctx.guild.id)

        try:
            del self.controllers[ctx.guild.id]
        except KeyError:
            await player.disconnect()
            return await ctx.send('Вышел')

        await player.disconnect()
        await ctx.send('Вышел')

    @commands.command(name='equalizer', description='Эквалайзер музыки, состоит из 15 уровней', aliases=['eq'])
    async def equalizer(self, ctx, equalizer='None'):
        """Change the players equalizer."""
        player = self.bot.wavelink.get_player(ctx.guild.id)

        if not player.is_connected:
            return

        predefiend = {'default': wavelink.Equalizer.flat(),
                      'boost': wavelink.Equalizer.boost(),
                      'metal': wavelink.Equalizer.metal(),
                      'piano': wavelink.Equalizer.piano()
                      }

        eq = predefiend.get(equalizer.lower(), None)

        if not eq or not equalizer:
            joined = "\n".join(predefiend.keys())
            return await ctx.send(f'Такого эквалайзера нет, доступны:\n{joined}')

        await player.set_eq(eq)
        await ctx.send(f'Поставил эквалайзер {equalizer}. Применение займет несколько секунд...')


def setup(bot):
    bot.add_cog(Music(bot))
