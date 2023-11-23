from discord import Interaction, app_commands
from .bonzoPlayer import BonzoPlayer

from ..exceptions  import CustomCheckError

async def get_player(inter: Interaction):
    if inter.guild.voice_client:
        return inter.guild.voice_client
    
    player = await inter.user.voice.channel.connect(cls=BonzoPlayer)
    await player.set_context(inter)
    return player


def same_voice():
    async def predicate(inter: Interaction):
        player: BonzoPlayer = await get_player(inter)

        if not player:
            return True
        
        if inter.user.voice.channel.id != player.channel.id:
            raise CustomCheckError(message="Ты должен быть в том же голосовом канале, что и бот!")
        return True
    
    return app_commands.check(predicate)

def author_in_voice():
    async def predicate(inter: Interaction):
        if not inter.user.voice:
            raise CustomCheckError(message="Ты должен быть в голосовом канале!")
        return True
    
    return app_commands.check(predicate)

def bot_in_voice():
    async def predicate(inter: Interaction):
        if not inter.guild.voice_client:
            raise CustomCheckError(message="Бот не находится в голосовом канале!")
        return True
    
    return app_commands.check(predicate)

def is_playing():
    async def predicate(inter: Interaction):
        player: BonzoPlayer = await get_player(inter)
        if not player.is_playing:
            raise CustomCheckError(message="Сейчас ничего не играет!")
        return True
    
    return app_commands.check(predicate)

