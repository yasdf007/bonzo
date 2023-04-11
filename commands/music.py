import pomice

from discord.ext.commands import hybrid_command, Context, Cog, CommandError
from discord import Member, VoiceState, Interaction
from discord.app_commands import Choice, autocomplete

from .resources.music.bonzoPlayer import BonzoPlayer
from .resources.music.checks import CustomCheckError, author_in_voice, bot_in_voice, get_player, is_playing, same_voice
from .resources.music.ui import DropdownView, Dropdown
from .resources.music.filters import equalizers

from bot import Bot
from config import lavalink_config

from typing import List

import logging
import re

TIME_REGEX = re.compile("([0-9]{1,2})m:([0-9]{1,2})s")

class Music(Cog):
    def __init__(self, bot):
        self.bot: Bot = bot

    async def cog_command_error(self, ctx: Context, error: CommandError):
        logging.warning(f"MUSIC ERROR: {error}")
        # if isinstance(error, CustomCheckError):
        #     return 
        # if isinstance(error, MissingRequiredArgument):
        #     return

        # logging.warning(f"MUSIC ERROR: {error}")
        # await ctx.send(f"Упс... кажется произошла неизвестная ошибка :(")
        # await ctx.voice_client.teardown()
        # # raise error

    async def start_nodes(self):
            await self.bot.wait_until_ready()
            await self.pomice.create_node(
                    bot=self.bot,
                    host=lavalink_config.host,
                    port=int(lavalink_config.port),
                    password=lavalink_config.password,
                    identifier="MAIN"
                )

    async def cog_load(self) -> None:
        self.pomice = pomice.NodePool()
        self.bot.loop.create_task(self.start_nodes())

    def check_status(self):
        node: pomice.Node = self.pomice.get_node()
        if not node.is_connected:
            raise CustomCheckError(message="Отсутствует соединение с проигрывателем!")
    
    @Cog.listener()
    async def on_voice_state_update(self, member: Member, before: VoiceState, after: VoiceState):
        if member.id != self.bot.user.id:
            return
        
        if before.channel and not after.channel:
            node: pomice.Node = self.pomice.get_node()
            if node:
                player: BonzoPlayer = node.get_player(member.guild.id)
                if player:
                    await player.teardown()

    @Cog.listener()
    async def on_pomice_track_end(self, player: BonzoPlayer, track, _):
        await player.do_next()

    @Cog.listener()
    async def on_pomice_track_stuck(self, player: BonzoPlayer, track: pomice.Track, error):
        logging.warning(f'on_pomice_track_stuck\n{error}')

        await player.context.send(f"Возникла ошибка при проигрывании  {track.title}")
        await player.do_next()

    @Cog.listener()
    async def on_pomice_track_exception(self, player: BonzoPlayer, track: pomice.Track, error):
        logging.warning(f'on_pomice_track_exception\n{error}')

        await player.context.send(f"Возникла ошибка при проигрывании {track.title}")
        await player.do_next()

    @hybrid_command(name='play', description="Ищет и играет музыку по ссылке или запросу.")
    @same_voice()
    @author_in_voice()
    async def play(self, ctx: Context, query: str):
        self.check_status()

        player: BonzoPlayer = await get_player(ctx)

        results = await player.get_tracks(query, ctx=ctx)
        if not results:
            raise CustomCheckError(message="Не найдено ни одного трека!")

        if isinstance(results, pomice.Playlist):
            for track in results.tracks:
                player.queue.put(track)
            await ctx.send(f"Плейлист с {results.track_count} треками добавлен в очередь")   
        else:
            track = results[0]
            player.queue.put(track)
            await ctx.send(f"{track.title} добавлен в очередь")   

        if not player.is_playing:
            await player.do_next()


    @hybrid_command(name='stop', description="Останавливает воспроизведение и отключается.")
    @same_voice()
    @author_in_voice()
    @bot_in_voice()
    async def stop(self, ctx: Context):
        self.check_status()

        player: BonzoPlayer = await get_player(ctx)
        await player.teardown()

        await ctx.send(f"Отключился из голосового канала.")

    @hybrid_command(name='skip', description="Пропускает текущую музыку.")
    @is_playing()
    @same_voice()
    @author_in_voice()
    @bot_in_voice()
    async def skip(self, ctx: Context):
        self.check_status()

        player: BonzoPlayer = await get_player(ctx)

        track = player.current
        await ctx.send(f"Пропустил {track.title}")
        await player.stop()

    @hybrid_command(name='search', description="Осуществляет поиск музыки.")
    @same_voice()
    @author_in_voice()
    async def search(self, ctx: Context, query: str):
        self.check_status()

        player: BonzoPlayer = await get_player(ctx)
        results = await player.get_tracks(query, ctx=ctx)
        if not results:
            raise CustomCheckError(message="Не найдено ни одного трека!")

        dropdown = Dropdown(results)
        view = DropdownView(ctx.author, dropdown, timeout=25)

        await ctx.send(f"Всего нашлось {len(results)} результатов", view=view)
        await view.wait()

        if view.dropdown.value != None:
            track = results[view.dropdown.value]
            player.queue.put(track)
            if not player.is_playing:
                await player.do_next()

    @hybrid_command(name='pause', description="Останавливает/возобновляет воспроизведение.")
    @is_playing()
    @same_voice()
    @author_in_voice()
    @bot_in_voice()
    async def pause(self, ctx: Context):
        self.check_status()
        
        player: BonzoPlayer = await get_player(ctx)

        if player.is_paused:
            await player.set_pause(False)
            return await ctx.send("Пауза убрана")
        else:
            await player.set_pause(True)
            return await ctx.send("Пауза поставлена")
        
    @hybrid_command(name='unpause', description="Возобновляет воспроизведение.")
    @is_playing()
    @same_voice()
    @author_in_voice()
    @bot_in_voice()
    async def unpause(self, ctx: Context):
        self.check_status()

        player: BonzoPlayer = await get_player(ctx)
        
        if not player.is_paused:
            raise CustomCheckError(message="Музыка не на паузе!")

        await player.set_pause(False)
        await ctx.send("Пауза убрана")
    # -------------------
    @hybrid_command(name='volume', description="Меняет громкость воспроизведение.")
    @is_playing()
    @same_voice()
    @author_in_voice()
    @bot_in_voice()
    async def volume(self, ctx: Context, volume: int):
        self.check_status()

        player: BonzoPlayer = await get_player(ctx)

        await player.set_volume(volume)
        await ctx.send(f"Установлена громкость: {volume}")

    async def equalizer_autocomplete(
            self,
            interaction: Interaction,
            current: str,
        ) -> List[Choice[str]]:
            return [
                Choice(name=filter, value=filter)
                for filter in ['default', 'bass'] if current.lower() in filter.lower()
            ]

    @hybrid_command(name='equalizer', description="Применяет пресет эквалайзера.")
    @is_playing()
    @same_voice()
    @author_in_voice()
    @bot_in_voice()
    @autocomplete(preset=equalizer_autocomplete)
    async def equalizer(self, ctx: Context, preset: str):
        self.check_status()

        player: BonzoPlayer = await get_player(ctx)
        eq = equalizers.get(preset)
        if not eq:
            raise CustomCheckError(message="Такого пресета эквалайзера нет!")

        await player.reset_filters()
        await player.add_filter(eq, fast_apply=True)

        await ctx.send(f"Применил пресет {preset}")

    @hybrid_command(name='reset_filters', description="Убирает фильтры.")
    @is_playing()
    @same_voice()
    @author_in_voice()
    @bot_in_voice()
    async def reset_filters(self, ctx: Context):
        self.check_status()

        player: BonzoPlayer = await get_player(ctx)
        try:
            await player.reset_filters(fast_apply=True)
        except pomice.exceptions.FilterInvalidArgument:
            pass

        await ctx.send(f"Убрал все фильтры")

    # -------------------

    @hybrid_command(name='now_playing', description="Показывает текущую музыку.", aliases=['np'])
    @is_playing()
    @author_in_voice()
    @bot_in_voice()
    async def now_playing(self, ctx: Context):
        self.check_status()

        player: BonzoPlayer = await get_player(ctx)
        
        await ctx.send(embed=await player.get_controller(player.current))

    @hybrid_command(name='loop', description="Ставит/убирает текущую музыку на повтор.")
    @is_playing()
    @same_voice()
    @author_in_voice()
    @bot_in_voice()
    async def loop(self, ctx: Context):
        self.check_status()

        player: BonzoPlayer = await get_player(ctx)
        if player.queue.is_looping:
            player.queue.disable_loop()
            return await ctx.send(f"{player.current.title} убран с повтора.")
        else:
            player.queue.set_loop_mode(pomice.LoopMode.TRACK)
            return await ctx.send(f"{player.current.title} поставлен на повтор.")

    @hybrid_command(name='shuffle', description="Перемешивает музыку в очереди.")
    @same_voice()
    @author_in_voice()
    @bot_in_voice()
    async def shuffle(self, ctx: Context):
        self.check_status()

        player: BonzoPlayer = await get_player(ctx)
        if len(player.queue) < 1:
            raise CustomCheckError(message="Очередь пустая, перемешивать нечего!")
        await ctx.send("Очередь перемешана")

        await player.shuffle()


    @hybrid_command(name='seek', description="Пропускает до таймкода в музыке (формат 0m:00s).")
    @is_playing()
    @same_voice()
    @author_in_voice()
    @bot_in_voice()
    async def seek(self, ctx: Context, time: str):
        self.check_status()

        player: BonzoPlayer = await get_player(ctx)
        
        match = TIME_REGEX.match(time)
        if not match:
            raise CustomCheckError(message="Неправильный формат времени!")
        
        milliseconds = (int(match.group(1)) * 60 + int(match.group(2))) * 1000

        await player.seek(milliseconds)

async def setup(bot):
    await bot.add_cog(Music(bot))
