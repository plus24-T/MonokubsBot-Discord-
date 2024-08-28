import os 
import discord.context_managers
from dotenv import load_dotenv
import discord
from discord import app_commands
from discord.ext import commands
import global_value as g

load_dotenv()

#キャラロール名からデータ格納変数名への変換辞書　要る？変数名直打ちすることないので要らないより
#                                               個人へのデータの紐づけ方法要検討　メンバーidの方がよさげ？
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

class AlEgo_Select(discord.ui.Select):
    def __init__(self,options:list[discord.SelectOption]):
        super().__init__(
            placeholder="対象を選択",
            options=options
            )
    async def callback(self, itx: discord.Interaction):
        if len(discord.utils.get(itx.guild.roles,name="死亡").members)==0:
           despair_threshold=3
        else:
           despair_threshold=4
        exec(f"role_id=g.{nick_to_data[self.values[0]]}")
        if role_id <=despair_threshold:
            await itx.response.send_message(f"『{self.values[0]}』は希望〈キボウ〉サイドです")
        else:
            if role_id != 6:
                await itx.response.send_message(f"『{self.values[0]}』は絶望〈ゼツボウ〉サイドです")
            else:
                #本当はここに絶望の残党の有無生存判定での分岐を追加する
                await itx.response.send_message(f"『{self.values[0]}』は絶望〈ゼツボウ〉サイドです")

        
        

class AlEgo_View(discord.ui.View):
    def __init__(self,options:list[discord.SelectOption]):
        super().__init__(timeout=180)

        self.add_item(AlEgo_Select(options=options))

class AlterEgo_ability(commands.Cog):#コマンド名、頭大文字でクラス作成
    def __init__(self, bot:commands.Bot):
        self.bot = bot

    @app_commands.command(
            name="alterego_ability",#coomand_nameがコマンドになる
            description="アルターエゴの判別対象を選択、判別結果を返します"#コマンドリストに表示される説明文
            )
    async def rehearsal(self, itx:discord.Interaction):#ここが処理内容、必要な引数とか設定する
        living_members = discord.utils.get(itx.guild.roles,name="生存").members
        select_op_living_members = []    #生存メンバーのリストから選択候補のリストを作成
        for member in living_members:
            select_op_living_members.append(discord.SelectOption(label=member.nick))#判別不可(モノクマのヘアゴム)対象を取り除く工程は未実装
        await itx.response.send_message("アルターエゴが判別対象を選択しています")
        await discord.utils.get(itx.guild.channels,name="アルターエゴ").send(#最終的には役職チャンネルなくして個人のプライベートチャンネルに投稿するように変更予定
            "判別の対象を選択してください",
            view=AlEgo_View(options=select_op_living_members)
            )

async def setup(bot:commands.Bot):
    await bot.add_cog(
        AlterEgo_ability(bot),
        guilds = [discord.Object(id=os.getenv("GUILD_ID"))]
        )
