import os 
import discord.context_managers
from dotenv import load_dotenv

import discord
from discord import app_commands
from discord.ext import commands
import gv

load_dotenv()

class Hagakure(commands.Cog):#コマンド名、頭大文字でクラス作成
    def __init__(self, bot:commands.Bot):
        self.bot = bot

    @app_commands.command(
            name="hagakure",#coomand_nameがコマンドになる
            description="葉隠の能力を使用します"#コマンドリストに表示される説明文
            
            )
    async def hagakure(self,itx:discord.Interaction, *, member: discord.Member): 
        if itx.channel.name != "葉隠康比呂":
            itx.response.send_message("自分の部屋でこっそり占うべ！\n（このチャンネルでは使用できません）")
        else:#プレイヤー数による患者との分岐は後回し（たぶんしばらく要らないため）
            if gv.nick_to_data[member.nick].role.id == 5:
                await itx.response.send_message(f"『{member.nick}』は モノミ だべ！")
            else:
                await itx.response.send_message(f"『{member.nick}』は モノミ じゃねえべ！")

async def setup(bot:commands.Bot):
    await bot.add_cog(
        Hagakure(bot),
        guilds = [discord.Object(id=os.getenv("GUILD_ID"))]
        )
