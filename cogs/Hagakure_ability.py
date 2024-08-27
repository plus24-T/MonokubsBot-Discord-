import os 
import discord.context_managers
from dotenv import load_dotenv

import discord
from discord import app_commands
from discord.ext import commands

load_dotenv()

class Hagakure(commands.Cog):#コマンド名、頭大文字でクラス作成
    def __init__(self, bot:commands.Bot):
        self.bot = bot

    @app_commands.command(
            name="hagakure",#coomand_nameがコマンドになる
            description="対象のキャラクターがモノミか判定します"#コマンドリストに表示される説明文
            )
    async def hagakure(self,itx:discord.Interaction, *, member: discord.Member):
        
        if discord.utils.get(itx.guild.roles,name="モノミ") in member.roles:
            await itx.response.send_message(f"『{member.nick}』は モノミ だべ！")
        else:
            await itx.response.send_message(f"『{member.nick}』は モノミ じゃねえべ！")

async def setup(bot:commands.Bot):
    await bot.add_cog(
        Hagakure(bot),
        guilds = [discord.Object(id=os.getenv("GUILD_ID"))]
        )
