import os 
import discord.context_managers

import discord
from discord import app_commands
from discord.ext import commands
import gv
import utils

class Megane_Select(discord.ui.Select):
    def __init__(self,options:list[discord.SelectOption]):
        super().__init__(
            placeholder="対象を選択",
            options=options,
            disabled=False
            )
    async def callback(self, itx: discord.Interaction):
        target_chara_name = self.values[0]
        is_despair = utils.check_despair(itx, target_chara_name)
        if is_despair:
            await itx.response.send_message(f"『{target_chara_name}』は絶望〈ゼツボウ〉サイドです")
        else:
            await itx.response.send_message(f"『{target_chara_name}』は希望〈キボウ〉サイドです")
        
        await discord.utils.get(itx.guild.channels,name="食堂").send("判別が終わりました")
        self.disabled=True

class Megane_View(discord.ui.View):
    def __init__(self,options:list[discord.SelectOption]):
        super().__init__(timeout=180)

        self.add_item(Megane_Select(options=options))

class Megane(commands.Cog):#コマンド名、頭大文字でクラス作成
    def __init__(self, bot:commands.Bot):
        self.bot = bot

    @app_commands.command(
            name="megane",#coomand_nameがコマンドになる
            description="おでこのメガネを使用します"#コマンドリストに表示される説明文            
            )
    async def megane(self,itx:discord.Interaction):
        if gv.chara_role_list.alterego[0] in discord.utils.get(itx.guild.roles,name="生存").members:
            await itx.response.send_message("おでこのメガネで、デコデコ、デコリ～ン！\n（使用条件：アルターエゴの死亡　を満たしていません）")
            pass 
        living_members = discord.utils.get(itx.guild.roles,name="生存").members
        select_op_living_members = []    #生存メンバーのリストから選択候補のリストを作成
        for member in living_members:
            select_op_living_members.append(discord.SelectOption(label=member.nick))
        await itx.response.send_message(f"{itx.user.nick}がおでこのメガネの力を行使しています、少々お待ちください")
        await discord.utils.get(itx.guild.channels,name=itx.user.nick).send(
            "判別の対象を選択してください",
            view=Megane_View(options=select_op_living_members)
            )

async def setup(bot:commands.Bot):
    await bot.add_cog(
        Megane(bot),
        guilds = [discord.Object(id=bot.useGuildId)]
        )
