import os 
import discord.context_managers

import discord
from discord import app_commands
from discord.ext import commands
import gv


class Album_Select(discord.ui.Select):
    def __init__(self,options:list[discord.SelectOption]):
        super().__init__(
            placeholder="対象を選択",
            options=options,
            disabled=False
            )
    async def callback(self, interaction: discord.Interaction):
        #プレイヤー数による患者との分岐は後回し（たぶんしばらく要らないため）
        if gv.get_chara_data(self.values[0]).role == gv.CharaRole.URAGIRI:
            await interaction.response.send_message(f"『{self.values[0]}』は 裏切者 です")
        else:
            await interaction.response.send_message(f"『{self.values[0]}』は 裏切者 ではありません")
        await discord.utils.get(interaction.guild.channels,name="食堂").send("調査が終わりました")
        self.disabled=True

class Album_View(discord.ui.View):
    def __init__(self,options:list[discord.SelectOption]):
        super().__init__(timeout=180)

        self.add_item(Album_Select(options=options))

class Album(commands.Cog):#Cog名、頭大文字でクラス作成
    def __init__(self, bot:commands.Bot):
        self.bot = bot

    @app_commands.command(
            name="album",#coomand_nameがコマンドになる
            description="誰かの卒業アルバムを使用します"#コマンドリストに表示される説明文            
            )
    async def album(self,interaction:discord.Interaction): 
        living_members = discord.utils.get(interaction.guild.roles,name="生存").members
        select_op_living_members = []    #生存メンバーのリストから選択候補のリストを作成
        for member in living_members:
            select_op_living_members.append(discord.SelectOption(label=member.nick))
        await interaction.response.send_message(f"{interaction.user.nick}が誰かの卒業アルバムを調べています、少々お待ちください")
        await discord.utils.get(interaction.guild.channels,name=interaction.user.nick).send(
            "判別の対象を選択してください",
            view=Album_View(options=select_op_living_members)
            )

async def setup(bot:commands.Bot):
    await bot.add_cog(
        Album(bot),
        guilds = [discord.Object(id=bot.useGuildId)]
        )
