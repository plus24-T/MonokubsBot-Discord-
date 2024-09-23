import os 
import discord.context_managers

import discord
from discord import app_commands
from discord.ext import commands


# 全ロール剥奪（松田夜助）
class Yasuke(commands.Cog):#コマンド名、頭大文字でクラス作成
    def __init__(self, bot:commands.Bot):
        self.bot = bot

    @app_commands.command(
            name="yasuke",#coomand_nameがコマンドになる
            description="全ての管理用サーバーロールを剥奪します"#コマンドリストに表示される説明文
            )
    async def yasuke(self, interaction:discord.Interaction):#ここが処理内容、必要な引数とか設定する
        await interaction.response.defer()
        guild = interaction.user.guild
        for member in guild.members:
            if member != guild.owner:
                if not member.bot:
                    for role in member.roles:
                        if role != guild.default_role:                                  
                            await member.remove_roles(role)
                            await member.edit(nick=None)
        await interaction.followup.send("ロールリセット処理は成功しました")

async def setup(bot:commands.Bot):
    await bot.add_cog(
        Yasuke(bot),
        guilds = [discord.Object(id=bot.useGuildId)]
        )
