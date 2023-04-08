from discord.ui import Select
from discord.ui.view import View
from discord import SelectOption, Interaction, Member

from typing import List
import pomice

class Dropdown(Select):
    def __init__(self, tracks: List[pomice.Track]):
        self.tracks = tracks
        self.value = None
        options = []

        for index, track in enumerate(tracks):
            options.append(SelectOption(label=track.title, value=index))

        super().__init__(placeholder='Выбери трек...', min_values=1, max_values=1, options=options)

    async def callback(self, interaction: Interaction):
        self.disabled = True
        self.value = int(self.values[0])
        self.placeholder = self.tracks[self.value].title
        self.disabled = True
        await interaction.response.edit_message(view=self.view)
        self.view.stop()

class DropdownView(View):
    def __init__(self, author: Member, dropdown: Dropdown, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.author = author
        self.dropdown = dropdown
        self.add_item(dropdown)

    async def on_timeout(self) -> None:
        self.clear_items()

    async def interaction_check(self, interaction: Interaction):
        if not interaction.user.id == self.author.id:
            await interaction.response.send_message(content="Невозможно произвести выбор!", ephemeral=True)
            return False
        return True