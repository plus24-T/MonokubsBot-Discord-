import os 
import discord.context_managers

import discord
from discord import app_commands
from discord.ext import commands
import gv


class Hagakure_Select(discord.ui.Select):
    def __init__(self,options:list[discord.SelectOption]):
        super().__init__(
            placeholder="対象を選択",
            options=options,
            disabled=False
            )
    async def callback(self, itx: discord.Interaction):
        #プレイヤー数による患者との分岐は後回し（たぶんしばらく要らないため）
        if gv.get_chara_data(self.values[0]).role == gv.CharaRole.MONOMI:
            await itx.response.send_message(f"『{self.values[0]}』は モノミ だべ！")
        else:
            await itx.response.send_message(f"『{self.values[0]}』は モノミ じゃねえべ！")
        await discord.utils.get(itx.guild.channels,name="食堂").send("占いが終わりました")
        self.disabled=True

class Hagakure_View(discord.ui.View):
    def __init__(self,options:list[discord.SelectOption]):
        super().__init__(timeout=180)

        self.add_item(Hagakure_Select(options=options))

class Hagakure(commands.Cog):#コマンド名、頭大文字でクラス作成
    def __init__(self, bot:commands.Bot):
        self.bot = bot

    @app_commands.command(
            name="hagakure",#coomand_nameがコマンドになる
            description="葉隠の能力を使用します"#コマンドリストに表示される説明文            
            )
    async def hagakure(self,itx:discord.Interaction): 
        living_members = discord.utils.get(itx.guild.roles,name="生存").members
        select_op_living_members = []    #生存メンバーのリストから選択候補のリストを作成
        for member in living_members:
            select_op_living_members.append(discord.SelectOption(label=member.nick))
        await itx.response.send_message("葉隠康比呂が占っています、少々お待ちください")
        await discord.utils.get(itx.guild.channels,name="葉隠康比呂").send(
            "判別の対象を選択してください",
            view=Hagakure_View(options=select_op_living_members)
            )

async def setup(bot:commands.Bot):
    await bot.add_cog(
        Hagakure(bot),
        guilds = [discord.Object(id=bot.useGuildId)]
        )
