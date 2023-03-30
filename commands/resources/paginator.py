# Paginator was initially created by another development team. 
# Bonzo utilizes paginator in order to make beautiful multi-page help messages.

# Пагинатор был изначально создан другой командой разработчиков.
# Бонзо использует пагинатор для создания красивых и многостраничных [b]/help ответов

from typing import Union
from asyncio import FIRST_COMPLETED as ASYNCIO_FIRST_COMPLETED
from asyncio import wait as asyncioWait
from asyncio import TimeoutError as AsyncioTimeoutError
from discord import errors
from discord import Embed


class Paginator:
    def __init__(self, ctx, reactions: Union[tuple, list] = None, timeout: int = 120):
        self.reactions = reactions or ('⬅', '⏹', '➡')
        self.pages = []
        self.current = 0
        self.ctx = ctx
        self.timeout = timeout

    async def _close_session(self):
        """Close current paginator session and delete message."""
        try:
            await self.controller.delete()
        except errors.NotFound:
            pass

        del self.pages
        del self.reactions
        del self.current
        del self.ctx

    def add_page(self, embed: Embed):
        self.pages.append(embed)

    async def call_controller(self, start_page: int = 0):
        """Call paginator interface.
        Parameters
        ----------
        start_page : int
          Start paginator from the given page (default: 0 - first page)
        """
        if start_page > len(self.pages) - 1:
            raise IndexError(f"Currently added {len(self.pages)} pages, but you"
                             f"tried to call controller with start_page = {start_page}")

        self.controller = await self.ctx.send(embed=self.pages[start_page])

        for emoji in self.reactions:
            await self.controller.add_reaction(emoji)

        def author_check(r, u): return u.id == self.ctx.author.id \
            and r.emoji in self.reactions and r.message.id == self.controller.id

        while True:
            try:
                tasks = [
                    self.ctx.bot.wait_for('reaction_add',
                                          timeout=self.timeout, check=author_check),
                    self.ctx.bot.wait_for('reaction_remove',
                                          timeout=self.timeout, check=author_check)]

                tasks_result, tasks = await asyncioWait(tasks, return_when=ASYNCIO_FIRST_COMPLETED)

                for task in tasks:
                    task.cancel()
                for task in tasks_result:
                    response = await task

            except AsyncioTimeoutError:
                break

            try:
                await self.controller.remove_reaction(response[0], response[1])
            except Exception:
                pass

            if response[0].emoji == self.reactions[0]:
                self.current = self.current - \
                    1 if self.current > 0 else len(self.pages) - 1
                await self.controller.edit(embed=self.pages[self.current])

            if response[0].emoji == self.reactions[1]:
                break

            if response[0].emoji == self.reactions[2]:
                self.current = self.current + \
                    1 if self.current < len(self.pages) - 1 else 0
                await self.controller.edit(embed=self.pages[self.current])

        await self._close_session()
