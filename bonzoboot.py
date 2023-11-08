"""
Created by ムAloneStranger (c) 2023.
файл-загрузчик бота.
осуществлять запуск только из этого файла.
"""

from bot import Bot, Fore, Style
from dependencies.repository.prefix.memory import PrefixRepositoryMemory
from database.memory.db import DictMemoryDB

if __name__ == "__main__":
    bot = Bot(PrefixRepositoryMemory(DictMemoryDB))

    bot.run()
