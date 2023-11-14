from discord import app_commands, Interaction
from config import OWNER_IDS
from .exceptions import NotOwner

def check_is_owner() -> bool:
    def predicate(interaction: Interaction) -> bool:
        if not interaction.user.id in OWNER_IDS:
            raise NotOwner() 
        return True
    return app_commands.check(predicate)
