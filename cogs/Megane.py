import os 
import discord.context_managers
from dotenv import load_dotenv

import discord
from discord import app_commands
from discord.ext import commands
import gv

load_dotenv()

class Megane_Select(discord.ui.Select):
    def __init__(self,options:list[discord.SelectOption]):
        super().__init__(
            placeholder="対象を選択",
            options=options,
            disabled=False
            )
    async def callback(self, itx: discord.Interaction):
        if len(discord.utils.get(itx.guild.roles,name="死亡").members)==0:
            despair_threshold=3
        else:
            despair_threshold=2

        if gv.nick_to_data[self.values[0]].role.id <=despair_threshold:
            await itx.response.send_message(f"『{self.values[0]}』は希望〈キボウ〉サイドです")
        else:
            if gv.nick_to_data[self.values[0]].role.id != 6:
                await itx.response.send_message(f"『{self.values[0]}』は絶望〈ゼツボウ〉サイドです")
            else:
                if len(gv.Cast.zantou)==0:
                    await itx.response.send_message(f"『{self.values[0]}』は絶望〈ゼツボウ〉サイドです")
                else:
                    if gv.Cast.zantou[0] in discord.utils.get(itx.guild.roles,name="死亡").members:
                        await itx.response.send_message(f"『{self.values[0]}』は絶望〈ゼツボウ〉サイドです")
                    else:
                        await itx.response.send_message(f"『{self.values[0]}』は希望〈キボウ〉サイドです")
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
        if gv.Cast.alterego[0] in discord.utils.get(itx.guild.roles,name="生存").members:
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
        guilds = [discord.Object(id=os.getenv("GUILD_ID"))]
        )
