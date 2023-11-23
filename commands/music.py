import pomice

from discord.ext.commands import Cog
from discord import Member, VoiceState, app_commands, Interaction
from discord.app_commands import Choice, autocomplete

from .resources.music.bonzoPlayer import BonzoPlayer
from .resources.music.checks import CustomCheckError, author_in_voice, bot_in_voice, get_player, is_playing, same_voice
from .resources.music.ui import DropdownView, Dropdown
from .resources.music.filters import equalizers

from bot import Bot
from config import LAVALINK_CONNECTION_OPTIONS

from typing import List

import logging
import re

TIME_REGEX = re.compile("([0-9]{1,2})m:([0-9]{1,2})s")

class Music(Cog):
    def __init__(self, bot):
        self.bot: Bot = bot

    async def start_nodes(self):
        await self.bot.wait_until_ready()
        await self.pomice.create_node(
                bot=self.bot,
                **LAVALINK_CONNECTION_OPTIONS,
            )

    async def cog_load(self) -> None:
        self.pomice = pomice.NodePool()
        self.bot.loop.create_task(self.start_nodes())

    def check_status(self, node: pomice.Node):
        if not node.is_connected:
            raise CustomCheckError(message="Отсутствует соединение с проигрывателем! Подождите некоторое время.")
    
    @Cog.listener()
    async def on_voice_state_update(self, member: Member, before: VoiceState, after: VoiceState):
        if member.id != self.bot.user.id:
            return
        
        node: pomice.Node = self.pomice.get_node()
        if not node:
            return

        player: BonzoPlayer = node.get_player(member.guild.id)
        if not player:
            return

        if before.channel and not after.channel:
            await player.teardown()
        
        if before.channel and after.channel:
            player(self.bot, after.channel)

    @Cog.listener()
    async def on_pomice_track_end(self, player: BonzoPlayer, track, _):
        await player.do_next()

    @Cog.listener()
    async def on_pomice_track_stuck(self, player: BonzoPlayer, track: pomice.Track, error):
        logging.warning(f'on_pomice_track_stuck\n{error}')

        await player.context.followup.send(f"Возникла ошибка при проигрывании  {track.title}")
        await player.do_next()
        
        raise error

    @Cog.listener()
    async def on_pomice_track_exception(self, player: BonzoPlayer, track: pomice.Track, error):
        logging.warning(f'on_pomice_track_exception\n{error}')

        await player.context.followup.send(f"Возникла ошибка при проигрывании {track.title}")
        await player.do_next()

        raise error

    @app_commands.command(name='play', description="Ищет и играет музыку по ссылке или запросу.")
    @same_voice()
    @author_in_voice()
    async def play(self, inter: Interaction, query: str):
        player: BonzoPlayer  = inter.guild.voice_client
        self.check_status(player.node)

        results = await player.get_tracks(query)
        if not results:
            raise CustomCheckError(message="Не найдено ни одного трека!")

        if isinstance(results, pomice.Playlist):
            for track in results.tracks:
                player.queue.put(track)
            await inter.response.send_message(f"Плейлист с {results.track_count} треками добавлен в очередь")   
        else:
            track = results[0]
            player.queue.put(track)
            await inter.response.send_message(f"{track.title} добавлен в очередь")   

        if not player.is_playing:
            await player.do_next()


    @app_commands.command(name='stop', description="Останавливает воспроизведение и отключается.")
    @same_voice()
    @bot_in_voice()
    @author_in_voice()
    async def stop(self, inter: Interaction):
        player: BonzoPlayer = await get_player(inter)
        await player.teardown()

        await inter.response.send_message(f"Отключился из голосового канала.")

    @app_commands.command(name='skip', description="Пропускает текущую музыку.")
    @is_playing()
    @same_voice()
    @bot_in_voice()
    @author_in_voice()
    async def skip(self, inter: Interaction):
        player: BonzoPlayer = await get_player(inter)
        self.check_status(player.node)

        track = player.current
        await inter.response.send_message(f"Пропустил {track.title}")
        try:
            await player.stop()
        except Exception as e:
            logging.warning(f"COULD NOT SKIP: {e}")

    @app_commands.command(name='search', description="Осуществляет поиск музыки.")
    @same_voice()
    @author_in_voice()
    async def search(self, inter: Interaction, query: str):
        player: BonzoPlayer = await get_player(inter)
        self.check_status(player.node)

        results = await player.get_tracks(query)
        if not results:
            raise CustomCheckError(message="Не найдено ни одного трека!")

        dropdown = Dropdown(results)
        view = DropdownView(inter.user, dropdown, timeout=25)

        await inter.response.send_message(f"Всего нашлось {len(results)} результатов", view=view)
        await view.wait()

        if view.dropdown.value != None:
            track = results[view.dropdown.value]
            player.queue.put(track)
            if not player.is_playing:
                await player.do_next()

    @app_commands.command(name='pause', description="Останавливает/возобновляет воспроизведение.")
    @is_playing()
    @same_voice()
    @bot_in_voice()
    @author_in_voice()
    async def pause(self, inter: Interaction):
        player: BonzoPlayer = await get_player(inter)
        self.check_status(player.node)

        if player.is_paused:
            await player.set_pause(False)
            return await inter.response.send_message("Пауза убрана")
        else:
            await player.set_pause(True)
            return await inter.response.send_message("Пауза поставлена")
        
    @app_commands.command(name='unpause', description="Возобновляет воспроизведение.")
    @is_playing()
    @same_voice()
    @bot_in_voice()
    @author_in_voice()
    async def unpause(self, inter: Interaction):
        player: BonzoPlayer = await get_player(inter)
        self.check_status(player.node)
        
        if not player.is_paused:
            raise CustomCheckError(message="Музыка не на паузе!")

        await player.set_pause(False)
        await inter.response.send_message("Пауза убрана")
    # -------------------
    @app_commands.command(name='volume', description="Меняет громкость воспроизведение.")
    @is_playing()
    @same_voice()
    @bot_in_voice()
    @author_in_voice()
    async def volume(self, inter: Interaction, volume: int):
        player: BonzoPlayer = await get_player(inter)
        self.check_status(player.node)

        await player.set_volume(volume)
        await inter.response.send_message(f"Установлена громкость: {volume}")

    async def equalizer_autocomplete(
            self,
            interaction: Interaction,
            current: str,
        ) -> List[Choice[str]]:
            return [
                Choice(name=filter, value=filter)
                for filter in ['default', 'bass'] if current.lower() in filter.lower()
            ]

    @app_commands.command(name='equalizer', description="Применяет пресет эквалайзера.")
    @is_playing()
    @same_voice()
    @bot_in_voice()
    @author_in_voice()
    @autocomplete(preset=equalizer_autocomplete)
    async def equalizer(self, inter: Interaction, preset: str):
        player: BonzoPlayer = await get_player(inter)
        self.check_status(player.node)

        eq = equalizers.get(preset)
        if not eq:
            raise CustomCheckError(message="Такого пресета эквалайзера нет!")

        await player.reset_filters()
        await player.add_filter(eq, fast_apply=True)

        await inter.response.send_message(f"Применил пресет {preset}")

    @app_commands.command(name='reset_filters', description="Убирает фильтры.")
    @is_playing()
    @same_voice()
    @bot_in_voice()
    @author_in_voice()
    async def reset_filters(self, inter: Interaction):
        player: BonzoPlayer = await get_player(inter)
        self.check_status(player.node)

        try:
            await player.reset_filters(fast_apply=True)
        except pomice.exceptions.FilterInvalidArgument:
            pass

        await inter.response.send_message(f"Убрал все фильтры")

    # -------------------

    @app_commands.command(name='now_playing', description="Показывает текущую музыку.")
    @is_playing()
    @bot_in_voice()
    @author_in_voice()
    async def now_playing(self, inter: Interaction):
        player: BonzoPlayer = await get_player(inter)
        self.check_status(player.node)
        
        await inter.response.send_message(embed=await player.get_controller(player.current))

    @app_commands.command(name='loop', description="Ставит/убирает текущую музыку на повтор.")
    @is_playing()
    @same_voice()
    @bot_in_voice()
    @author_in_voice()
    async def loop(self, inter: Interaction):
        player: BonzoPlayer = await get_player(inter)
        self.check_status(player.node)

        if player.queue.is_looping:
            player.queue.disable_loop()
            return await inter.response.send_message(f"{player.current.title} убран с повтора.")
        else:
            player.queue.set_loop_mode(pomice.LoopMode.TRACK)
            return await inter.response.send_message(f"{player.current.title} поставлен на повтор.")

    @app_commands.command(name='shuffle', description="Перемешивает музыку в очереди.")
    @same_voice()
    @bot_in_voice()
    @author_in_voice()
    async def shuffle(self, inter: Interaction):
        player: BonzoPlayer = await get_player(inter)
        self.check_status(player.node)

        if len(player.queue) < 1:
            raise CustomCheckError(message="Очередь пустая, перемешивать нечего!")
        await inter.response.send_message("Очередь перемешана")

        await player.shuffle()


    @app_commands.command(name='seek', description="Пропускает до таймкода в музыке (формат 0m:00s).")
    @is_playing()
    @same_voice()
    @bot_in_voice()
    @author_in_voice()
    async def seek(self, inter: Interaction, time: str):
        player: BonzoPlayer = await get_player(inter)
        self.check_status(player.node)
        
        match = TIME_REGEX.match(time)
        if not match:
            raise CustomCheckError(message="Неправильный формат времени!")
        
        milliseconds = (int(match.group(1)) * 60 + int(match.group(2))) * 1000

        await player.seek(milliseconds)

async def setup(bot):
    await bot.add_cog(Music(bot))
