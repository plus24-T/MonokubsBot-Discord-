import os 
import discord.context_managers
from dotenv import load_dotenv

import discord
from discord import app_commands
from discord.ext import commands
import gv

load_dotenv()

#キャラ名からデータクラスへの変換辞書
nick_to_data={
    "苗木誠":gv.CC_02,
    "舞園さやか":gv.CC_03,
    "桑田怜恩":gv.CC_04,
    "霧切響子":gv.CC_05,
    "十神白夜":gv.CC_06,
    "山田一二三":gv.CC_07,
    "大和田紋土":gv.CC_08,
    "腐川冬子":gv.CC_09,
    "セレスティアルーデンベルク":gv.CC_10,
    "朝日奈葵":gv.CC_11,
    "石丸清多夏":gv.CC_12,
    "大神さくら":gv.CC_13,
    "葉隠康比呂":gv.CC_14,
    "江ノ島盾子":gv.CC_15,
    "不二咲千尋":gv.CC_16,
    "ジェノサイダー翔":gv.CC_17,
    "戦刃むくろ":gv.CC_18,
    "江ノ島盾子：絶望":gv.CC_19,
    "霧切響子：カップ麵":gv.MCC_01,
    "石丸清多夏：石田":gv.MCC_08,
    "江ノ島盾子：王冠":gv.MCC_09,
    "日向創":gv.CC_20,
    "狛枝凪斗":gv.CC_21,
    "田中眼蛇夢":gv.CC_22,
    "左右田和一":gv.CC_23,
    "十神白夜：ジャバウォック島のすがた":gv.CC_24,
    "花村輝々":gv.CC_25,
    "弐大猫丸":gv.CC_26,
    "九頭龍冬彦":gv.CC_27,
    "終里赤音":gv.CC_28,
    "七海千秋":gv.CC_29,
    "ソニアネヴァーマインド":gv.CC_30,
    "西園寺日寄子":gv.CC_31,
    "小泉真昼":gv.CC_32,
    "罪木蜜柑":gv.CC_33,
    "澪田唯吹":gv.CC_34,
    "辺古山ペコ":gv.CC_35,
    "狛枝凪斗：絶望":gv.MCC_02,
    "左右田和一：楳図かずお画風":gv.MCC_03,
    "十神白夜：腕組み":gv.MCC_05,
    "花村輝々：鼻血":gv.MCC_07,
    "弐大猫丸：メカ":gv.MCC_10,
    "七海千秋：唾吐き":gv.MCC_06,
    "西園寺日寄子：てへぺろ":gv.MCC_04
}

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
            if nick_to_data[member.nick].role.id == 5:
                await itx.response.send_message(f"『{member.nick}』は モノミ だべ！")
            else:
                await itx.response.send_message(f"『{member.nick}』は モノミ じゃねえべ！")

async def setup(bot:commands.Bot):
    await bot.add_cog(
        Hagakure(bot),
        guilds = [discord.Object(id=os.getenv("GUILD_ID"))]
        )
