from discord import Embed, app_commands, Interaction
from discord.ext.commands import Cog
from bot import Bot
from .resources.views import help
from math import ceil

name = "help"
description = "Все команды бота, инфа о команде help <cmd>"


class HelpCog(Cog):
    def __init__(self, bot):
        self.bot: Bot = bot
        self.cmds = []

    async def cog_load(self):

        cmd_ids = {}
        slash_commands = await self.bot.tree.fetch_commands()
        
        for cmd in slash_commands:
            cmd_ids[cmd.name] = cmd.id

        self.cmd_to_id = cmd_ids

    def get_commands(self):
        cmds = []
        cmd: app_commands.Command
        for cmd in self.bot.tree.get_commands():
            if isinstance(cmd, app_commands.Group):
                for subcommand in cmd.commands:
                    cmds.append(f'</{cmd.name} {subcommand.name}:{self.cmd_to_id[cmd.name]}> - {subcommand.description}')
            else:
                cmds.append(f'</{cmd.name}:{self.cmd_to_id[cmd.name]}> - {cmd.description}')
        
        self.cmds = cmds
        return cmds
    
    @app_commands.command(name=name, description=description)
    async def help(self, inter: Interaction, cmd: str = None):
        cmds = self.cmds
        if not cmds:
            cmds = self.get_commands()
           
        embed = help.build_help_embed(cmds[:10], 1, ceil(len(cmds) / 10))

        await inter.response.send_message(embed=embed, view=help.HelpView(cmds, 10))
        
async def setup(bot):
    await bot.add_cog(HelpCog(bot))
