import os

import discord
from discord import app_commands
from discord.ext import commands 
import discord.context_managers

from typing import List

import gv


class Tsumiki_Select(discord.ui.Select):
    def __init__(self,options:list[discord.SelectOption]):
        super().__init__(
            placeholder="今死亡したキャラクターを選んでください",
            options=options,
            disabled=False
            )
    async def callback(self, interaction: discord.Interaction):
        await interaction.response.send_message(f"『{self.values[0]}』は{gv.get_chara_data(self.values[0]).role.to_japanese_name()}でした")
        await discord.utils.get(interaction
        .guild.channels,name="食堂").send(f"{self.values[0]}の検死が終わりました")
        self.disabled=True

class Tsumiki_View(discord.ui.View):
    def __init__(self,options:list[discord.SelectOption]):
        super().__init__(timeout=180)

        self.add_item(Tsumiki_Select(options=options))

class Tsumiki(commands.Cog):#コマンド名、頭大文字でクラス作成
    def __init__(self, bot:commands.Bot):
        self.bot = bot

    @app_commands.command(
            name="tsumiki",#coomand_nameがコマンドになる
            description="罪木蜜柑の能力を処理します"#コマンドリストに表示される説明文
            )
    async def tsumiki(self, interaction:discord.Interaction):#ここが処理内容、必要な引数とか設定する
        dead_members = discord.utils.get(interaction.guild.roles,name="死亡").members
        select_op_dead_members = []    #死亡メンバーのリストから選択候補のリストを作成（本当は死亡直後なので選べないキャラが混じるがとりあえず）
        for member in dead_members:
            select_op_dead_members.append(discord.SelectOption(label=member.nick))
        await interaction.response.send_message("罪木蜜柑が遺体の検死をしています、少々お待ちください")
        await discord.utils.get(interaction.guild.channels,name="罪木蜜柑").send(
            "ロールを見る対象を選択してください",
            view=Tsumiki_View(options=select_op_dead_members)
            )

async def setup(bot:commands.Bot):
    await bot.add_cog(
        Tsumiki(bot),
        guilds = [discord.Object(id=bot.useGuildId)]
        )
