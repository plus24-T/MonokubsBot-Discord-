import os 
import discord.context_managers

import discord
from discord import app_commands
from discord.ext import commands
import gv
import utils

class Kirigiri_Select(discord.ui.Select):
    def __init__(self,options:list[discord.SelectOption]):
        super().__init__(
            placeholder="対象を選択",
            options=options,
            disabled=False
            )
    async def callback(self, interaction: discord.Interaction):
        target_chara_name = self.values[0]
        is_despair = utils.check_despair(interaction, target_chara_name)
        if is_despair:
            await interaction.response.send_message(f"『{target_chara_name}』は絶望〈ゼツボウ〉サイドです")
        else:
            await interaction.response.send_message(f"『{target_chara_name}』は希望〈キボウ〉サイドです")

        await discord.utils.get(interaction.guild.channels,name="食堂").send("推理がまとめ終わったようです")
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
    async def kirigiri(self,interaction:discord.Interaction):
        if gv.table_data.day <= 3:
            await interaction.response.send_message("霧切響子「推理をまとめるにはまだ証拠が足りないわ」\n（使用条件：４日目以降を満たしていません）")
            pass 
        living_members = discord.utils.get(interaction.guild.roles,name="生存").members
        select_op_living_members = []    #生存メンバーのリストから選択候補のリストを作成
        for member in living_members:
            select_op_living_members.append(discord.SelectOption(label=member.nick))
        await interaction.response.send_message("霧切響子が推理をまとめています、少々お待ちください")
        await discord.utils.get(interaction.guild.channels,name="霧切響子").send(
            "判別の対象を選択してください",
            view=Kirigiri_View(options=select_op_living_members)
            )

async def setup(bot:commands.Bot):
    await bot.add_cog(
        Kirigiri(bot),
        guilds = [discord.Object(id=bot.useGuildId)]
        )
