import os
from typing import List 
import discord.context_managers
from discord.utils import MISSING
from dotenv import load_dotenv

import discord
from discord import app_commands
from discord.ext import commands

load_dotenv()

class Rehearsal_Select(discord.ui.Select):
    def __init__(self,options:list[discord.SelectOption]):
        super().__init__(
            placeholder="対象を選択",
            options=options
            )
    async def callback(self, itx: discord.Interaction):
        await itx.response.edit_message(f"『{self.values[0]}』の部屋を荒らしました")
        await discord.utils.get(itx.guild.channels,name=self.values[0]).send(
            "あなたの部屋が荒らされました、手持ちのアイテムを1枚選択して裏向きのまま捨てて下さい"
            )
        await discord.utils.get(itx.guild.channels,name="食堂").send(f"{self.values[0]}の部屋が荒らされました")

class Rehearsal_View(discord.ui.View):
    def __init__(self,living_menbers:list[discord.SelectOption]):
        super().__init__(timeout=180)

        self.add_item(options=living_menbers)

class Rehearsal(commands.Cog):#コマンド名、頭大文字でクラス作成
    def __init__(self, bot:commands.Bot):
        self.bot = bot

    @app_commands.command(
            name="rehearsal",#coomand_nameがコマンドになる
            description="0日目夜のクロの下見を行います"#コマンドリストに表示される説明文
            )
    async def rehearsal(self, itx:discord.Interaction):#ここが処理内容、必要な引数とか設定する
        living_members = discord.utils.get(itx.guild.roles,name="生存").members
        voting_destinations = []    #生存メンバーのリストから投票先候補のリストを作成
        for member in living_members:
            voting_destinations.append(discord.SelectOption(label=member.nick))
        await itx.response.send_message("クロが下見の対象を選択しています")
        await discord.utils.get(itx.guild.channels,name="クロ").send(
            "下見の対象を選択してください",
            view=Rehearsal_View(living_menbers=living_members)
            )

async def setup(bot:commands.Bot):
    await bot.add_cog(
        Rehearsal(bot),
        guilds = [discord.Object(id=os.getenv("GUILD_ID"))]
        )
