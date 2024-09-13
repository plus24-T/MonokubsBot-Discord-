import os 

from typing import List, Literal

import discord
import discord.context_managers
from discord import app_commands
from discord.ext import commands

import gv


class Add_dead_role(commands.Cog):#Cog名、任意だが分かりやすさのためにコマンドが一つなら頭大文字でクラス作成
    def __init__(self, bot:commands.Bot):
        self.bot = bot

    @app_commands.command(
            name="死亡ロール付与",#coomand_nameがコマンドになる
            description="襲撃とおしおきの死亡者登録するやつ"#コマンドリストに表示される説明文
            )
    async def add_dead_role(self, itx:discord.Interaction,死因:Literal["襲撃","おしおき"],死者:discord.Member):#ここが処理内容、必要な引数とか設定する
        if 死因=="襲撃":
            gv.table_data.kill+=1
            await itx.response.send_message(f"襲撃により{死者.nick}は死亡しました")
            死者.remove_roles(discord.utils.get(itx.guild.roles,name="生存"))
            死者.add_roles(discord.utils.get(itx.guild.roles,name="死亡"))
        else:
            await itx.response.send_message(f"{死者.nick}はおしおきされました")
            死者.remove_roles(discord.utils.get(itx.guild.roles,name="生存"))
            死者.add_roles(discord.utils.get(itx.guild.roles,name="死亡"))
            if gv.get_chara_data(死者.nick).role == gv.CharaRole.TYOZETSUBO:
                await itx.followup.send(f"{死者.nick}は超高校級の絶望でした\n\n{死者.nick}の勝利です")

async def setup(bot:commands.Bot):
    await bot.add_cog(
        Add_dead_role(bot),
        guilds = [discord.Object(id=bot.useGuildId)]
        )
