import os 
import discord.context_managers

import discord
from discord import app_commands
from discord.ext import commands
import gv


class Kirigiri_Select(discord.ui.Select):
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
        await discord.utils.get(itx.guild.channels,name="食堂").send("推理がまとめ終わったようです")
        self.disabled=True

class Kirigiri_View(discord.ui.View):
    def __init__(self,options:list[discord.SelectOption]):
        super().__init__(timeout=180)

        self.add_item(Kirigiri_Select(options=options))

class Kirigiri(commands.Cog):#コマンド名、頭大文字でクラス作成
    def __init__(self, bot:commands.Bot):
        self.bot = bot

    @app_commands.command(
            name="kirigiri",#coomand_nameがコマンドになる
            description="霧切響子の能力を使用します"#コマンドリストに表示される説明文            
            )
    async def kirigiri(self,itx:discord.Interaction):
        if gv.day <= 3:
            await itx.response.send_message("霧切響子「推理をまとめるにはまだ証拠が足りないわ」\n（使用条件：４日目以降を満たしていません）")
            pass 
        living_members = discord.utils.get(itx.guild.roles,name="生存").members
        select_op_living_members = []    #生存メンバーのリストから選択候補のリストを作成
        for member in living_members:
            select_op_living_members.append(discord.SelectOption(label=member.nick))
        await itx.response.send_message("霧切響子が推理をまとめています、少々お待ちください")
        await discord.utils.get(itx.guild.channels,name="霧切響子").send(
            "判別の対象を選択してください",
            view=Kirigiri_View(options=select_op_living_members)
            )

async def setup(bot:commands.Bot):
    await bot.add_cog(
        Kirigiri(bot),
        guilds = [discord.Object(id=bot.useGuildId)]
        )
