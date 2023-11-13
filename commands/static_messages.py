from discord import app_commands, Interaction, Embed, Color
from discord.ext.commands import Cog
from bot import Bot


class StaticMessages(Cog):
    def __init__(self, bot):
        self.bot: Bot = bot

    @app_commands.command(name='donate', description='Пожертвования разработчикам bonzo')
    async def donate(self, inter: Interaction):
        donate_embed = build_donate_embed()
        await inter.response.send_message(embed=donate_embed)

    @app_commands.command(name='init', description='Краткая информация об использовании бота / How to start?')
    async def inita(self, inter: Interaction):
        inita_embed = build_bot_init_message('b/')
        await inter.response.send_message(embed=inita_embed)

    @app_commands.command(name='invite', description='Ссылка на приглашение бота')
    async def invite_bot(self, inter: Interaction):
        invite_embed = build_invite_embed(inter.user.name)
        await inter.response.send_message(embed=invite_embed)

async def setup(bot):
    await bot.add_cog(StaticMessages(bot))


qiwilink = "https://qiwi.com/n/OTTIC882"
telegdonate = "https://t.me/CryptoBot?start=IV8duUiKkI7K"

def build_donate_embed():
    embed = Embed(
        title="**Способы пожертвований средств разработчикам Bonzo**",
        color=Color.random(),
    )
    embed.set_thumbnail(url="https://i.ibb.co/Xk7qTy4/BOnzo-1.png")
    embed.add_field(
        name="**Для пожертвования через QIWI (RUB):**",
        value=f"**-->** [QIWI/RUB]({qiwilink}) **<--**",
    )
    embed.add_field(
        name="**Для пожертвований с помощью криптовалют:**",
        value=f"**-->** [TELEGRAM/CRYPTO]({telegdonate}) **<--**",
    )
    embed.set_footer(text="/by bonzo/ for THE best! ^-^")

    return embed
    

supportserver = "https://discord.gg/kjUdcUGw"

def build_bot_init_message(prefix):
    embed = Embed(title="**Начало работы с bonzo**", color=Color.random())

    embed.set_thumbnail(url="https://i.ibb.co/Xk7qTy4/BOnzo-1.png")

    embed.add_field(
        name="**Для использования legacy-команд:**", value=f"{prefix}help"
    )
    embed.add_field(name="**Для использования slash-команд:**", value="/help_slash")
    embed.add_field(
        name="**Для изменения префикса:**", value="@Bonzo set_prefix [ваш префикс]"
    )
    embed.add_field(
        name="**Для связи с разработчиками:**",
        value=f"[Перейдите на сервер (нажмите сюда)]({supportserver})",
    )

    embed.set_footer(text="/by bonzo/ for everyone :)")
    
    return embed

invlink = "https://discord.com/api/oauth2/authorize?client_id=680132907859443790&permissions=8&scope=bot%20applications.commands"

def build_invite_embed(for_username):
    embedd = Embed(title="**Зовём /bonzo/ на Ваш сервер...**", colour=0xB84000)
    embedd.set_thumbnail(url="https://i.ibb.co/Xk7qTy4/BOnzo-1.png")
    embedd.add_field(
        name="Спасибо за поддержку!",
        value=f"**-->** [Нажмите сюда!]({invlink}) **<--**",
    )
    embedd.set_footer(text=f"/by bonzo/ for @{for_username}")

    return embedd