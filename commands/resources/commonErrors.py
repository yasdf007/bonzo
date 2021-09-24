from discord import Embed
from .animationFW import randCol

class Errors:
    
    NoCmd = Embed(
        title='**Команда не найдена**',
        color=randCol()
    )

    NoUrl = Embed(
        title='**Ссылка не найдена**',
        color=randCol()
    )

    RequestNetworkError = Embed(
        title='**Не удалось открыть файл**',
        color=randCol()
    )

    TooManySymbols = Embed(
        title='**Максимум 25 символов**',
        color=randCol()
    )
    
    FileTooLarge = Embed(
        title='**Максимальный размер файла - 5МБ**',
        color=randCol()
    )

    InvalidType = Embed(
        title='**Неподдерживаемый формат файла - доступны png, jpeg и jpg**',
        color=randCol()
    )

