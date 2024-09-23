import os 

from typing import List, Literal

import discord
import discord.context_managers
from discord import app_commands
from discord.ext import commands

import gv


class ItemEffectRegistration(commands.Cog):#Cog名、任意だが分かりやすさのためにコマンドが一つなら頭大文字でクラス作成
    def __init__(self, bot:commands.Bot):
        self.bot = bot

    @app_commands.command(
            name="アイテム効果登録",#coomand_nameがコマンドになる
            description="アイテム効果登録するやつ"#コマンドリストに表示される説明文
            )
    async def item_effect_registration(self, interaction:discord.Interaction,効果:Literal["襲撃無効","二票持ち"],target_nickname:discord.Member):#ここが処理内容、必要な引数とか設定する
        if 効果=="襲撃無効":
            gv.get_chara_data(target_nickname).escorted=True
            await interaction.response.send_message(f"{target_nickname.nick}に襲撃無効が付与されました")

        else:
            gv.get_chara_data(target_nickname).votes=2
            await interaction.response.send_message(f"{target_nickname.nick}は次の投票で2票投票できます")

async def setup(bot:commands.Bot):
    await bot.add_cog(
        ItemEffectRegistration(bot),
        guilds = [discord.Object(id=bot.useGuildId)]
        )
