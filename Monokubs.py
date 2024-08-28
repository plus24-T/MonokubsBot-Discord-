import os
import collections
import dataclasses
from dotenv import load_dotenv
from typing import List, Literal
import discord
from discord.ext import commands

load_dotenv()#環境変数の読み込み

Test_GUILD = discord.Object(id=os.getenv("GUILD_ID"))#テスト鯖のIDからテスト鯖オブジェクトを取得 
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

#キャラの役職パラメータと役職名の変換辞書
role_para_to_name:dict = {
    0:"シロ",
    1:"アルターエゴ",
    2:"未来機関",#ここまで希望判定
    3:"超高校級の絶望",#死亡者の有無で判別の閾値を変更して対応
    4:"絶望病患者",#ここから絶望判定
    5:"モノミ",
    6:"クロ",
    7:"裏切者",
    8:"ザコケモノ",
    9:"絶望の残党"
    }
role_name_to_para:dict = {
    "シロ":0,
    "アルターエゴ":1,
    "未来機関":2,#ここまで希望判定
    "超高校級の絶望":3,#死亡者の有無で判別の閾値を変更して対応
    "絶望病患者":4,#ここから絶望判定
    "モノミ":5,
    "クロ":6,
    "裏切者":7,
    "ザコケモノ":8,
    "絶望の残党":9
    }
#キャラロール名からデータ格納変数名への変換辞書　要る？変数名直打ちすることないので要らないより
#                                               個人へのデータの紐づけ方法要検討　メンバーidの方がよさげ？
nick_to_data={
    "苗木誠":"naegi_data",
    "舞園さやか":"maizono_data",
    "桑田怜恩":"kuwata_data",
    "霧切響子":"kirigiri_data",
    "十神白夜":"togami_data",
    "山田一二三":"yamada_data",
    "大和田紋土":"oowada_data",
    "腐川冬子":"hukawa_data",
    "セレスティアルーデンベルク":"seresu_data",
    "朝日奈葵":"asahina_data",
    "石丸清多夏":"ishimaru_data",
    "大神さくら":"oogami_data",
    "葉隠康比呂":"hagakure_data",
    "江ノ島盾子":"enoshima_data",
    "不二咲千尋":"hujisaki_data",
    "ジェノサイダー翔":"syo_data",
    "戦刃むくろ":"ikusaba_data",
    "江ノ島盾子：絶望":"enoshima_despair_dta",
    "霧切響子：カップ麵":"kirigiri_m_data",
    "石丸清多夏：石田":"isida_data",
    "江ノ島盾子：王冠":"enoshima_m_data",
    "日向創":"hinata_data",
    "狛枝凪斗":"komaeda_data",
    "田中眼蛇夢":"tanaka_data",
    "左右田和一":"souda_data",
    "十神白夜：ジャバウォック島のすがた":"togami_2_data",
    "花村輝々":"hanamura_data",
    "弐大猫丸":"nidai_data",
    "九頭龍冬彦":"kuzuryu_data",
    "終里赤音":"owari_data",
    "七海千秋":"nanami:data",
    "ソニアネヴァーマインド":"sonia_data",
    "西園寺日寄子":"saionji_data",
    "小泉真昼":"koizumi_data",
    "罪木蜜柑":"tsumiki_data",
    "澪田唯吹":"mioda_data",
    "辺古山ペコ":"pekoyama_data",
    "狛枝凪斗：絶望":"komaeda_m_data",
    "左右田和一：楳図かずお画風":"souda_m_data",
    "十神白夜：腕組み":"togami_m_data",
    "花村輝々：鼻血":"hanamura_m_data",
    "弐大猫丸：メカ":"nidai_m_data",
    "七海千秋：唾吐き":"nanami_m_data",
    "西園寺日寄子：てへぺろ":"saionji_m_data"
}


        # 読み込むcogsのリストを作る
initial_extensions = [
    "ext_test",
    "Hagakure_ability",
    "Yasuke",
    "Reearsal"
]
#botのインスタンス化と起動時の処理
class MonokubsBot(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix=commands.when_mentioned_or('!'),# メンション若しくは!でコマンドを認識する　あんまり使わないけど
            intents=discord.Intents.all()# すべてのインテント権限をTureにする
            )


    # セットアップ時の処理
    async def setup_hook(self) -> None:

        self.add_view(RoleSleMenu())# view(ボタンやセレクトメニュー)のBotへの取り込み

        for cog in initial_extensions:
            await self.load_extension(f"cogs.{cog}")# コマンドやイベント処理のBotへの取り込み
        try:
            synced = await bot.tree.sync(guild=Test_GUILD)# コマンドをDiscordに同期、鯖指定で反映を即時にしている
            print(f"synced {len(synced)} commands ")
        except Exception as e:
            print(e)
                
    # 起動時処理＆確認
    async def on_ready(self):
        #アクティビティを設定
        new_activity = f"テスト" 
        await bot.change_presence(activity=discord.Game(new_activity)) 
        print(f'Logged in as {self.user} (ID: {self.user.id})')#ログインしたやでとターミナルに出力
        print('------')

bot = MonokubsBot()

#自動リネーム機能　及び　ロール付与に反応するやつ全般　最終的に死亡時処理だけになりそう
@bot.event 
async def on_member_update(before:discord.Member, after:discord.Member):
    guild = before.guild

    #各ロールの変数への代入
    ROLE_START = discord.utils.get(guild.roles, name="西園寺日寄子：てへぺろ")
    ROLE_END = discord.utils.get(guild.roles, name="苗木誠")
    ROLE_DIE = discord.utils.get(guild.roles,name="死亡")

    #付加されたロールと剥奪されたロールのリストを取得
    roles_before = set(before.roles)
    roles_after = set(after.roles)
    
    added_roles = roles_after - roles_before
    removed_roles = roles_before - roles_after

    
    #自動リネーム
    for role in added_roles:
        if ROLE_START <= role <= ROLE_END:
            try:
                await after.edit(nick=role.name)
                break
            except Exception as e:
                print(e)
            

    for role in removed_roles:
        if ROLE_START <= role <= ROLE_END:
            await after.edit(nick=None)
            break
   
    #アルターエゴ死亡時　自動ロール開示
    if not added_roles.isdisjoint([ROLE_DIE]):
        if nick_to_data[after.nick].role.id == 1:
            await discord.utils.get(guild.channels,name="食堂").send(f"『{after.nick}』はアルターエゴでした")



# キャラクターセレクト　1，2選択ボタン→セレクトメニュー　そのうち最初から1、2、1バレ無、2バレ無のセレクト出す形にする

class CharaSleMenu1(discord.ui.View): # UIキットを利用するためにdiscord.ui.Viewを継承する
    def __init__(self, timeout=180): # Viewにはtimeoutがあり、初期値は180(s)である
        super().__init__(timeout=timeout)

    @discord.ui.select(
        cls=discord.ui.Select,
        placeholder="キャラクターを選択",
        options=[
            discord.SelectOption(label="苗木誠"),
            discord.SelectOption(label="舞園さやか"),
            discord.SelectOption(label="桑田怜恩"),
            discord.SelectOption(label="霧切響子"),
            discord.SelectOption(label="十神白夜"),
            discord.SelectOption(label="山田一二三"),
            discord.SelectOption(label="大和田紋土"),
            discord.SelectOption(label="腐川冬子"),
            discord.SelectOption(label="セレスティアルーデンベルク"),
            discord.SelectOption(label="朝日奈葵"),
            discord.SelectOption(label="石丸清多夏"),
            discord.SelectOption(label="大神さくら"),
            discord.SelectOption(label="葉隠康比呂"),
            discord.SelectOption(label="江ノ島盾子"),
            discord.SelectOption(label="不二咲千尋"),
            discord.SelectOption(label="ジェノサイダー翔"),
            discord.SelectOption(label="戦刃むくろ"),
            discord.SelectOption(label="江ノ島盾子：絶望"),
            discord.SelectOption(label="霧切響子：カップ麵"),
            discord.SelectOption(label="石丸清多夏：石田"),
            discord.SelectOption(label="江ノ島盾子：王冠"),
        ]
    )
    async def select(self, interaction: discord.Interaction, select: discord.ui.Select):
        await interaction.user.add_roles(discord.utils.get(interaction.guild.roles, name=select.values[0]))
        nick_to_data[select.values[0]]=CharaData(chara_ability=select.values[0])
        await interaction.user.add_roles(discord.utils.get(interaction.guild.roles, name="生存"))#いずれ鯖からキャラロール消してここでリネームする
        await interaction.response.send_message("よくきたな、" + select.values[0] )

class CharaSleMenu2(discord.ui.View): # UIキットを利用するためにdiscord.ui.Viewを継承する
    def __init__(self, timeout=180): # Viewにはtimeoutがあり、初期値は180(s)である
        super().__init__(timeout=timeout)

    @discord.ui.select(
        cls=discord.ui.Select,
        placeholder="キャラクターを選択",
        options=[
            discord.SelectOption(label="日向創"),
            discord.SelectOption(label="狛枝凪斗"),
            discord.SelectOption(label="田中眼蛇夢"),
            discord.SelectOption(label="左右田和一"),
            discord.SelectOption(label="十神白夜：ジャバウォック島のすがた"),
            discord.SelectOption(label="花村輝々"),
            discord.SelectOption(label="弐大猫丸"),
            discord.SelectOption(label="九頭龍冬彦"),
            discord.SelectOption(label="終里赤音"),
            discord.SelectOption(label="七海千秋"),
            discord.SelectOption(label="ソニアネヴァーマインド"),
            discord.SelectOption(label="西園寺日寄子"),
            discord.SelectOption(label="小泉真昼"),
            discord.SelectOption(label="罪木蜜柑"),
            discord.SelectOption(label="澪田唯吹"),
            discord.SelectOption(label="辺古山ペコ"),
            discord.SelectOption(label="狛枝凪斗：絶望"),
            discord.SelectOption(label="左右田和一：楳図かずお画風"),
            discord.SelectOption(label="十神白夜：腕組み"),
            discord.SelectOption(label="花村輝々：鼻血"),
            discord.SelectOption(label="弐大猫丸：メカ"),
            discord.SelectOption(label="七海千秋：唾吐き"),
            discord.SelectOption(label="西園寺日寄子：てへぺろ"),
        ]
    )
    async def select(self, interaction: discord.Interaction, select: discord.ui.Select):
        await interaction.user.add_roles(discord.utils.get(interaction.guild.roles, name=select.values[0]))
        await interaction.user.add_roles(discord.utils.get(interaction.guild.roles, name="生存"))
        await interaction.response.send_message("よくきたな、" + select.values[0] )

class CharaSleButton1(discord.ui.View): # UIキットを利用するためにdiscord.ui.Viewを継承する
    def __init__(self, timeout=180): # Viewにはtimeoutがあり、初期値は180(s)である
        super().__init__(timeout=timeout)

    @discord.ui.button(label="無印(1)", style=discord.ButtonStyle.primary) # OKボタン、押すとOKと返信する
    async def ok(self, interaction: discord.Interaction, button: discord.ui.Button):
        view = CharaSleMenu1(timeout=None)
        await interaction.response.send_message(view=view)

    @discord.ui.button(label="スーパー(2)", style=discord.ButtonStyle.primary) # NGボタン、押すとNGと返信する
    async def ng(self, interaction: discord.Interaction, button: discord.ui.Button):
        view = CharaSleMenu2(timeout=None)
        await interaction.response.send_message(view=view)

@bot.tree.command(name="monotaro",
                  description="キャラクターを選択し、管理用のサーバーロールを取得します",
                  guild=Test_GUILD
                  )
async def chara_select(itx:discord.Interaction):
    testembed = discord.Embed(
        title="キャラクター選択",
        description="おはっくまー！\nオマエはどちらから来た誰さん？\n\n（キャラカードを参照し、登場作品を選択）"
        )
    view = CharaSleButton1(timeout=None)
    await itx.response.send_message(embed=testembed,view=view)

# 役職ロールセレクトメニュー
class RoleSleMenu(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.select(
        cls=discord.ui.Select,
        placeholder="ロールカードに記載の役職を選択",
        options=[
            discord.SelectOption(label="シロ"),
            discord.SelectOption(label="クロ"),
            discord.SelectOption(label="アルターエゴ"),
            discord.SelectOption(label="裏切者"),
            discord.SelectOption(label="モノミ"),
            discord.SelectOption(label="超高校級の絶望"),
            discord.SelectOption(label="絶望病患者"),
            discord.SelectOption(label="ザコケモノ"),
            discord.SelectOption(label="未来機関"),
            discord.SelectOption(label="絶望の残党"),       
        ],
        custom_id="role_sle_menu"
    )
    async def select(self, itx: discord.Interaction, select: discord.ui.Select):
        await itx.user.add_roles(discord.utils.get(itx.guild.roles, name=select.values[0]))
        nick_to_data[itx.user.nick].role.name=select.values[0]
        nick_to_data[itx.user.nick].role.id=role_name_to_para[select.values[0]]
        if 6 <= role_name_to_para[select.values[0]] <= 7:
            await discord.utils.get(itx.guild.channels,name="裏切者").send(f"『{itx.user.nick}』は『{select.values[0]}』です")
        await itx.response.send_message("オマエニ、" + select.values[0] + " ノ、ロールヲ付与シマシタ", ephemeral=True)

@bot.tree.command(name="monodam",description="自身の役職を選択し、管理用のサーバーロールを取得します",guild=Test_GUILD)
@commands.is_owner()
async def monodam(itx: discord.Interaction):
    await itx.response.send_message("ロール選択ヲ、オ願イスルヨ",view=RoleSleMenu())

# helloコマンド
@bot.tree.command(name='hello', description='Say hello to the world!',guild=Test_GUILD) 
async def hello(itx: discord.Interaction): 
    await itx.response.send_message('Hello, World!')

#おしおき先投票機能（キャラアビ、アイテム未考慮）

voting_results = []

class Punishment_poll_select(discord.ui.Select): 
    def __init__(self, options: list[discord.SelectOption]) -> None:
        super().__init__(
            placeholder="投票先を選択",
            options=options
            )
    async def callback(self, itx: discord.Interaction):
        value = self.values[0]
        voting_results.append(value)
        await itx.response.send_message(f"『{value}』に投票しました、集計をお待ちください",ephemeral=True)
        if len(voting_results) == len(discord.utils.get(itx.guild.roles,name="生存").members):
            counted_result=collections.Counter(voting_results)#(投票先,得票数)のリストを作成
            saita_tokuhyo=counted_result.most_common()[0][1]#得票数多い順に並べ替えて最多得票数を取得
            tokuhyo = counted_result.values()#得票数だけのリストを取得
            if list(tokuhyo).count(saita_tokuhyo) == 1:#得票数の中に最多得票数が一つだけなら、つまり単独1位なら
                await itx.followup.send(f"きょうの〈おしおき〉は『{counted_result.most_common()[0][0]}』に決まりました")
                await discord.utils.get(itx.guild.members,nick=counted_result.most_common()[0][0]).remove_roles(discord.utils.get(itx.guild.roles,name="生存"))
                await discord.utils.get(itx.guild.members,nick=counted_result.most_common()[0][0]).add_roles(discord.utils.get(itx.guild.roles,name="死亡"))
                voting_results.clear()
            else:#単独一位とちゃうかったら
                finalists=[]
                for i in range(0,list(tokuhyo).count(saita_tokuhyo)):#[0,1,...,同率1位の数-1]に対してfor
                    finalists.append(discord.SelectOption(label=counted_result.most_common()[i][0]))#得票数i+1位の候補をリストに追加
                voting_results.clear()
                await itx.followup.send("決戦投票",view=Punishment_poll(options=finalists))#候補者差し替えて再度投票メニュー出す
                
class Punishment_poll(discord.ui.View):#投票セレクトメニューに変数（候補リスト）渡すためのView
    def __init__(self, options: list[discord.SelectOption]):
        super().__init__(timeout=180)
        
        self.add_item(Punishment_poll_select(options=options))

@bot.tree.command(name="make_punishment_poll",description="おしおき先の投票メニューを出します",guild=Test_GUILD)
async def make_punishment_poll(itx:discord.Interaction):
    living_members = discord.utils.get(itx.guild.roles,name="生存").members
    voting_destinations = []    #生存メンバーのリストから投票先候補のリストを作成
    for member in living_members:
        voting_destinations.append(discord.SelectOption(label=member.nick))

    await itx.response.send_message(
        "きょうの〈おしおき〉は誰かな～",
        view=Punishment_poll(options=voting_destinations)
        )

# ロールチェックコマンド　最終的に生存、死亡、GM、管理者？、Bot専用ロールのみにするので機能しなくなる　W.I.P
@bot.tree.command(name="check_role",description="対象者が該当ロールをもっているか判別します",guild=Test_GUILD)
async def test(itx:discord.Interaction, *, member: discord.Member, role: discord.Role):
    if role in member.roles:
        await itx.response.send_message(f"{member.nick} は {role.name} ロールを持っています。")
    else:
        await itx.response.send_message(f"{member.nick} は {role.name} ロールを持っていません。")

# エクステンションリロードする奴　リファクタリング不十分で活かしきれてないやつ
@bot.tree.command(name="ext_reload",description="(開発用)エクステンションをリロードします",guild=Test_GUILD)

async def ext_reload(
    itx:discord.Interaction,
    ext_name:Literal[#initial_extentionsから引っ張ってきたいけどなんかダメそう
        "ext_test",
        "Hagakure_ability",
        "Yasuke",
        "Rehearsal"
    ]
):
    await bot.reload_extension(ext_name)
    try:
        synced = await bot.tree.sync(guild=Test_GUILD)#コマンド同期しとかないとオートフィルでもうない変数要求されたりするので
        print(f"synced {len(synced)} commands ")
    except Exception as e:
        print(e)
    await itx.response.send_message(f"{ext_name}のリロードが完了しました",ephemeral=True)

bot.run(os.getenv("TOKEN"))