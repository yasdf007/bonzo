from discord.ext.commands import CheckFailure
from typing import Optional, Any
from discord.ext.commands import Context, check
import pomice
from .bonzoPlayer import BonzoPlayer


class CustomCheckError(CheckFailure):
    message: str = None
    def __init__(self, message: Optional[str] = None, *args: Any) -> None:
        self.message = message
        super().__init__(message, *args)


async def get_player(ctx: Context):
    if ctx.voice_client:
        return ctx.voice_client
    
    player = await ctx.author.voice.channel.connect(cls=BonzoPlayer)
    await player.set_context(ctx)
    return player


def author_in_voice():
    async def predicate(ctx: Context):
        if not ctx.author.voice:
            raise CustomCheckError(message="Ты должен быть в голосовом канале!")
        return True
    
    return check(predicate)

def bot_in_voice():
    async def predicate(ctx: Context):
        if not ctx.me.voice:
            raise CustomCheckError(message="Бот не находится в голосовом канале!")
        return True
    
    return check(predicate)

def is_playing():
    async def predicate(ctx: Context):
        player: BonzoPlayer = await get_player(ctx)
        if not player.is_playing:
            raise CustomCheckError(message="Сейчас ничего не играет!")
        return True
    
    return check(predicate)

