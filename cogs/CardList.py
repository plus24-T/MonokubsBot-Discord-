import os 
import discord.context_managers

import discord
from discord import app_commands
from discord.ext import commands

import Paginator

#試作中！
# Create a list of embeds to paginate.
embeds = [discord.Embed(title="First embed"),
          discord.Embed(title="Second embed"),
          discord.Embed(title="Third embed")
          ]
class CardList(commands.Cog):
    def __init__(self, bot:commands.Bot):
        self.bot = bot


    @app_commands.command(
            name="card_list",#comand_nameがコマンドになる
            description="ページ送り型のカードリスト出す奴"#コマンドリストに表示される説明文
            )
    async def card_list(self, interaction
                        :discord.Interaction):#ここが処理内容、必要な引数とか設定する
        await Paginator.Simple().start(interaction, pages=embeds)

async def setup(bot:commands.Bot):
    await bot.add_cog(
        CardList(bot),
        guilds = [discord.Object(id=bot.useGuildId)]
        )
