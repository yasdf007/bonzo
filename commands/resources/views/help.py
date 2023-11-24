from discord.ui import View, button, Button
from discord import enums, Interaction, Embed
from math import ceil

def build_help_embed(cmds, page, pages):
    embed = Embed(title="Команды бота")
    embed.add_field(name='Команды', value='\n'.join(cmds))
    embed.set_footer(text=f'Страница {page}/{pages}')
    return embed

class HelpView(View):
    def __init__(self, commands_info, per_page):
        super().__init__(timeout=180)
        self.commands_info = commands_info
        self.page = 1
        self.per_page = per_page
        self.pages = ceil(len(commands_info) / self.per_page)
    
    @button(emoji='⬅', style=enums.ButtonStyle.success)
    async def prev_page(self, inter: Interaction, button: Button):
        self.page -= 1
        if self.page < 1:
            self.page = 1 

        start = (self.page - 1) * self.per_page
        end = self.page*self.per_page
        cmds = self.commands_info[start:end]

        await inter.response.edit_message(embed=build_help_embed(cmds, self.page, self.pages), view=self)

    @button(emoji='➡', style=enums.ButtonStyle.success)
    async def next_page(self, inter: Interaction, button: Button):
        self.page += 1
        if self.page > self.pages:
            self.page = 1 

        start = (self.page - 1) * self.per_page
        end = self.page*self.per_page
        cmds = self.commands_info[start:end]

        await inter.response.edit_message(embed=build_help_embed(cmds, self.page, self.pages), view=self)
