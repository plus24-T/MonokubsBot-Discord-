import os 
import discord.context_managers
from dotenv import load_dotenv

import discord
from discord import app_commands
from discord.ext import commands
import gv

load_dotenv()

class SilentPhone_Select(discord.ui.Select):
    def __init__(self,options:list[discord.SelectOption]):
        super().__init__(
            placeholder="対象を選択",
            options=options,
            disabled=False
            )
    async def callback(self, itx: discord.Interaction):
        if gv.nick_to_data[self.values[0]].role.id == 0:
            await itx.response.send_message(f"『{self.values[0]}』は シロ です")
        else:
            await itx.response.send_message(f"『{self.values[0]}』は シロ ではありません")
        await discord.utils.get(itx.guild.channels,name="食堂").send("電話の呼び出し音は鳴りやんだようだ")
        self.disabled=True

class SilentPhone_View(discord.ui.View):
    def __init__(self,options:list[discord.SelectOption]):
        super().__init__(timeout=180)

        self.add_item(SilentPhone_Select(options=options))

class SilentPhone(commands.Cog):#コマンド名、頭大文字でクラス作成
    def __init__(self, bot:commands.Bot):
        self.bot = bot

    @app_commands.command(
            name="silent_phone",#coomand_nameがコマンドになる
            description="無言電話を使用します"#コマンドリストに表示される説明文            
            )
    async def silent_phone(self,itx:discord.Interaction): 
        living_members = discord.utils.get(itx.guild.roles,name="生存").members
        select_op_living_members = []    #生存メンバーのリストから選択候補のリストを作成
        for member in living_members:
            select_op_living_members.append(discord.SelectOption(label=member.nick))
        await itx.response.send_message(f"{itx.user.nick}が電話をかけています、少々お待ちください")
        await discord.utils.get(itx.guild.channels,name=itx.user.nick).send(
            "判別の対象を選択してください",
            view=SilentPhone_View(options=select_op_living_members)
            )

async def setup(bot:commands.Bot):
    await bot.add_cog(
        SilentPhone(bot),
        guilds = [discord.Object(id=os.getenv("GUILD_ID"))]
        )