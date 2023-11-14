from discord.ext.commands import CommandError
from typing import Any
from discord.app_commands.errors import CheckFailure, AppCommandError

class CustomCheckError(CommandError, AppCommandError):
    message: str = ''
    def __init__(self, message: str, *args: Any) -> None:
        self.message = message
        super().__init__(message, *args)

class NotOwner(CheckFailure): 
    def __init__(self) -> None:
        super().__init__('Not owner')