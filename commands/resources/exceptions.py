from discord.ext.commands import CommandError
from typing import Any

class CustomCheckError(CommandError):
    message: str = ''
    def __init__(self, message: str, *args: Any) -> None:
        self.message = message
        super().__init__(message, *args)
