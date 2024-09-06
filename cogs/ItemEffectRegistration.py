import os 
from dotenv import load_dotenv

from typing import List, Literal

import discord
import discord.context_managers
from discord import app_commands
from discord.ext import commands

import gv

load_dotenv()

class ItemEffectRegistration(commands.Cog):#Cog名、任意だが分かりやすさのためにコマンドが一つなら頭大文字でクラス作成
    def __init__(self, bot:commands.Bot):
        self.bot = bot

    @app_commands.command(
            name="アイテム効果登録",#coomand_nameがコマンドになる
            description="アイテム効果登録するやつ"#コマンドリストに表示される説明文
            )
    async def item_effect_registration(self, itx:discord.Interaction,効果:Literal["襲撃無効","二票持ち"],対象:discord.Member):#ここが処理内容、必要な引数とか設定する
        if 効果=="襲撃無効":
            gv.nick_to_data[対象].escorted=True
            await itx.response.send_message(f"{対象.nick}に襲撃無効が付与されました")

        else:
            gv.nick_to_data[対象].votes=2
            await itx.response.send_message(f"{対象.nick}は次の投票で2票投票できます")

async def setup(bot:commands.Bot):
    await bot.add_cog(
        ItemEffectRegistration(bot),
        guilds = [discord.Object(id=os.getenv("GUILD_ID"))]
        )
