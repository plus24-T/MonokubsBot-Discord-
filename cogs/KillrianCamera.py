import os
from dotenv import load_dotenv

import discord
from discord import app_commands
from discord.ext import commands 
import discord.context_managers

from typing import List

import gv

load_dotenv()

class KillrianCamera_Select(discord.ui.Select):
    def __init__(self,options:list[discord.SelectOption]):
        super().__init__(
            placeholder="対象を選択",
            options=options,
            disabled=False
            )
    async def callback(self, itx: discord.Interaction):
        await itx.response.send_message(f"『{self.values[0]}』は{gv.nick_to_data[self.values[0]].role.name}でした")
        await discord.utils.get(itx.guild.channels,name="食堂").send(f"{self.values[0]}の撮影が終わりました")
        self.disabled=True

class KillrianCamera_View(discord.ui.View):
    def __init__(self,options:list[discord.SelectOption]):
        super().__init__(timeout=180)

        self.add_item(KillrianCamera_Select(options=options))

class KillrianCamera(commands.Cog):#コマンド名、頭大文字でクラス作成
    def __init__(self, bot:commands.Bot):
        self.bot = bot

    @app_commands.command(
            name="killrian_camera",#coomand_nameがコマンドになる
            description="キルリアンカメラの能力を処理します"#コマンドリストに表示される説明文
            )
    async def killrian_camera(self, itx:discord.Interaction,user:discord.Member):#ここが処理内容、必要な引数とか設定する
        dead_members = discord.utils.get(itx.guild.roles,name="死亡").members
        select_op_dead_members = []    #死亡メンバーのリストから選択候補のリストを作成
        for member in dead_members:
            select_op_dead_members.append(discord.SelectOption(label=member.nick))
        await itx.response.send_message("心霊写真の撮影を試みています、少々お待ちください")
        await discord.utils.get(itx.guild.channels,name=user.nick).send(
            "ロールを見る対象を選択してください",
            view=KillrianCamera_View(options=select_op_dead_members)
            )

async def setup(bot:commands.Bot):
    await bot.add_cog(
        KillrianCamera(bot),
        guilds = [discord.Object(id=os.getenv("GUILD_ID"))]
        )