import os
from dotenv import load_dotenv

import discord
from discord import app_commands
from discord.ext import commands 
import discord.context_managers

from typing import List

import gv

load_dotenv()

class Rehearsal_Select(discord.ui.Select):
    def __init__(self,options:list[discord.SelectOption]):
        super().__init__(
            placeholder="対象を選択",
            options=options,
            disabled=False
            )
    async def callback(self, itx: discord.Interaction):
        await itx.response.send_message(f"『{self.values[0]}』の部屋を荒らしました")
        gv.day+=1
        await discord.utils.get(itx.guild.channels,name=self.values[0]).send(
            "あなたの部屋が荒らされました、手持ちのアイテムを1枚選択して裏向きのまま捨てて下さい"
            )
        await discord.utils.get(itx.guild.channels,name="食堂").send(f"オハヨウゴザイマス\n{gv.day}日目の朝時間になりました")
        await discord.utils.get(itx.guild.channels,name="食堂").send(f"{self.values[0]}の部屋が荒らされました")
        self.disabled=True

class Rehearsal_View(discord.ui.View):
    def __init__(self,options:list[discord.SelectOption]):
        super().__init__(timeout=180)

        self.add_item(Rehearsal_Select(options=options))

class Rehearsal(commands.Cog):#コマンド名、頭大文字でクラス作成
    def __init__(self, bot:commands.Bot):
        self.bot = bot

    @app_commands.command(
            name="rehearsal",#coomand_nameがコマンドになる
            description="0日目夜のクロの下見を行います"#コマンドリストに表示される説明文
            )
    async def rehearsal(self, itx:discord.Interaction):#ここが処理内容、必要な引数とか設定する
        living_members = discord.utils.get(itx.guild.roles,name="生存").members
        select_op_living_members = []    #生存メンバーのリストから選択候補のリストを作成
        for member in living_members:
            select_op_living_members.append(discord.SelectOption(label=member.nick))
        await itx.response.send_message("クロが下見の対象を選択しています")
        await discord.utils.get(itx.guild.channels,name=gv.Cast.kuro[0].nick).send(#最終的には役職チャンネルなくして個人のプライベートチャンネルに投稿するように変更予定
            "下見の対象を選択してください",
            view=Rehearsal_View(options=select_op_living_members)
            )

async def setup(bot:commands.Bot):
    await bot.add_cog(
        Rehearsal(bot),
        guilds = [discord.Object(id=os.getenv("GUILD_ID"))]
        )
