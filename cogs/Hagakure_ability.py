import os 
import discord.context_managers
from dotenv import load_dotenv

import discord
from discord import app_commands
from discord.ext import commands
import dataclasses
import gv

load_dotenv()

#参加キャラのデータを格納するクラス
@dataclasses.dataclass#役職のデータを格納するクラス
class CharaRole:
    id:int=0#役職に対応した数字、下記変換辞書参照
    name:str="未定"#役職の名前
@dataclasses.dataclass
class CharaData:
    role:CharaRole= dataclasses.field(default_factory=CharaRole)#役職idとname
    chara_ability:str=""#キャラ名（石田のコピー時ここを変えて参照する）
    ability_use:bool=True#キャラ能力使用状況（True：未使用、False：使用済み）
    num_of_items:int=0#所持アイテム数
    item_1_id:int=0#所持アイテム一つ目 intじゃ情報足りないので辞書咬ませてデータクラスとかになりそう
    item_2_id:int=0#所持アイテム二つ目
    votes:int=1#所持票数（投票無効時0にする）
    item_use:bool=1#各時間帯のアイテム使用権（Ture：未使用、False：使用済み）
    not_attacked:bool=False#襲撃されない（True：されない、False：される）
    unidentifiable:bool=False#判別不可（True：されない、False：される）
    escorted:bool=False#護衛されているか（True：されている、False：されていない）
    position=int#席の位置、生存人数の剰余で隣り合っているか判定する

nick_to_data={
    "苗木誠":"CC_02",
    "舞園さやか":"CC_03",
    "桑田怜恩":"CC_04",
    "霧切響子":"CC_05",
    "十神白夜":"CC_06",
    "山田一二三":"CC_07",
    "大和田紋土":"CC_08",
    "腐川冬子":"CC_09",
    "セレスティアルーデンベルク":"CC_10",
    "朝日奈葵":"CC_11",
    "石丸清多夏":"CC_12",
    "大神さくら":"CC_13",
    "葉隠康比呂":"CC_14",
    "江ノ島盾子":"CC_15",
    "不二咲千尋":"CC_16",
    "ジェノサイダー翔":"CC_17",
    "戦刃むくろ":"CC_18",
    "江ノ島盾子：絶望":"CC_19",
    "霧切響子：カップ麵":"MCC_01",
    "石丸清多夏：石田":"MCC_08",
    "江ノ島盾子：王冠":"MCC_09",
    "日向創":"CC_20",
    "狛枝凪斗":"CC_21",
    "田中眼蛇夢":"CC_22",
    "左右田和一":"CC_23",
    "十神白夜：ジャバウォック島のすがた":"CC_24",
    "花村輝々":"CC_25",
    "弐大猫丸":"CC_26",
    "九頭龍冬彦":"CC_27",
    "終里赤音":"CC_28",
    "七海千秋":"CC_29",
    "ソニアネヴァーマインド":"CC_30",
    "西園寺日寄子":"CC_31",
    "小泉真昼":"CC_32",
    "罪木蜜柑":"CC_33",
    "澪田唯吹":"CC_34",
    "辺古山ペコ":"CC_35",
    "狛枝凪斗：絶望":"MCC_02",
    "左右田和一：楳図かずお画風":"MCC_03",
    "十神白夜：腕組み":"MCC_05",
    "花村輝々：鼻血":"MCC_07",
    "弐大猫丸：メカ":"MCC_10",
    "七海千秋：唾吐き":"MCC_06",
    "西園寺日寄子：てへぺろ":"MCC_04"
}


class Hagakure(commands.Cog):#コマンド名、頭大文字でクラス作成
    def __init__(self, bot:commands.Bot):
        self.bot = bot

    @app_commands.command(
            name="hagakure",#coomand_nameがコマンドになる
            description="対象のキャラクターが絶望病患者（モノミ）か否か判別します"#コマンドリストに表示される説明文
            )
    async def hagakure(self,itx:discord.Interaction, *, member: discord.Member):
        exec(f"id=gv.{nick_to_data[member.nick]}.role.id")
        if id == 5:
            await itx.response.send_message(f"『{member.nick}』は モノミ だべ！")
        else:
            await itx.response.send_message(f"『{member.nick}』は モノミ じゃねえべ！")

async def setup(bot:commands.Bot):
    await bot.add_cog(
        Hagakure(bot),
        guilds = [discord.Object(id=os.getenv("GUILD_ID"))]
        )
