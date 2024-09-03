import os
import collections
import dataclasses
from dotenv import load_dotenv
from typing import List, Literal
import discord
from discord.ext import commands
import gv 

load_dotenv()#環境変数の読み込み

Test_GUILD = discord.Object(id=os.getenv("GUILD_ID"))#テスト鯖のIDからテスト鯖オブジェクトを取得

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

        # 読み込むcogsのリストを作る
initial_extensions = [
    "ext_test",
    "Hagakure_ability",
    "Yasuke",
    "Rehearsal",
    "Night",
    "Tsumiki"
    "KillrianCamera",
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
        self.add_view(CharaSleMenu1())#Viewにカスタムidを設定したうえでこれをしておくと
        self.add_view(CharaSleMenu2())#Botを立ち上げなおしてもボタン類が機能するようになる
        self.add_view(CharaSleMenuC1())
        self.add_view(CharaSleMenuC2())

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
    for role in removed_roles:
        if ROLE_START <= role <= ROLE_END:
            try:#鯖製作者の表示名変更権限はどうやっても得られないためtryでエラー回避
                await after.edit(nick=None)#Noneを代入するとニックネーム未設定に戻る
                break
            except Exception as e:
                print(e)
   
    #アルターエゴ死亡時　自動ロール開示
    if not added_roles.isdisjoint([ROLE_DIE]):
        if gv.nick_to_data[after.nick].role.id == 1:
            await discord.utils.get(guild.channels,name="食堂").send(f"『{after.nick}』はアルターエゴでした")
    #クロ死亡時　自動ロール開示　ゲーム終了
    if not added_roles.isdisjoint([ROLE_DIE]):
        if gv.nick_to_data[after.nick].role.id == 6:
            await discord.utils.get(guild.channels,name="食堂").send(f"『{after.nick}』はクロでした\n\n希望サイドの勝利です")

#プレイヤー人数登録

@bot.tree.command(name="input_number_of_players",
                  description="プレイ人数(GM除く)をbotに登録します",
                  guild=Test_GUILD
                  )
async def chara_select(itx:discord.Interaction,num:Literal[4,5,6,7,8,9,10,11,12,13,14,15,16]):

    gv.player=num
    await itx.response.send_message(f"今回のGMを除いたゲーム参加者は{num}人で登録しました\n"
                                    "誤入力の場合は再度登録しなおしてください\n"
                                    "※生存者数ではないのでゲーム進行により死亡キャラクターが\n"
                                    "発生しても更新する必要はありません")

# キャラクターセレクト
class CharaSleMenu1(discord.ui.View): # UIキットを利用するためにdiscord.ui.Viewを継承する
    def __init__(self): # Viewにはtimeoutがあり、初期値は180(s)である
        super().__init__(timeout=None)

    @discord.ui.select(
        cls=discord.ui.Select,
        placeholder="1（無印）",
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
        ],
        custom_id="charasle1"
    )
    async def select(self, interaction: discord.Interaction, select: discord.ui.Select):
        await interaction.user.add_roles(discord.utils.get(interaction.guild.roles, name=select.values[0]))
    
        gv.nick_to_data[select.values[0]].chara_ability=select.values[0]
        await interaction.user.add_roles(discord.utils.get(interaction.guild.roles, name="生存"))
        try:
            await interaction.user.edit(nick=select.values[0])
        except Exception as e:
            print(e)
        await interaction.response.send_message(
            f"よくきたな{select.values[0]}\nさっさと"
            f"{discord.utils.get(interaction.guild.channels,name=select.values[0]).mention}"
            "に移動してロールを登録してくるんだな"
            )

class CharaSleMenu2(discord.ui.View): # UIキットを利用するためにdiscord.ui.Viewを継承する
    def __init__(self): # Viewにはtimeoutがあり、初期値は180(s)である
        super().__init__(timeout=None)

    @discord.ui.select(
        cls=discord.ui.Select,
        placeholder="2（SUPER）",
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
        ],
        custom_id="charasle2"
    )
    async def select(self, interaction: discord.Interaction, select: discord.ui.Select):
        await interaction.user.add_roles(discord.utils.get(interaction.guild.roles, name=select.values[0]))
        gv.nick_to_data[select.values[0]].chara_ability=select.values[0]
        await interaction.user.add_roles(discord.utils.get(interaction.guild.roles, name="生存"))
        try:
            await interaction.user.edit(nick=select.values[0])
        except Exception as e:
            print(e)
        await interaction.response.send_message(
            f"よくきたな{select.values[0]}\nさっさと"
            f"{discord.utils.get(interaction.guild.channels,name=select.values[0]).mention}"
            "に移動してロールを登録してくるんだな"
            )

class CharaSleMenuC1(discord.ui.View): # UIキットを利用するためにdiscord.ui.Viewを継承する
    def __init__(self): # Viewにはtimeoutがあり、初期値は180(s)である
        super().__init__(timeout=None)

    @discord.ui.select(
        cls=discord.ui.Select,
        placeholder="ネタバレ配慮　1（無印）",
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
        ],
        custom_id="charaslelessbare1"
    )
    async def select(self, interaction: discord.Interaction, select: discord.ui.Select):
        await interaction.user.add_roles(discord.utils.get(interaction.guild.roles, name=select.values[0]))
        gv.nick_to_data[select.values[0]].chara_ability=select.values[0]
        await interaction.user.add_roles(discord.utils.get(interaction.guild.roles, name="生存"))
        try:
            await interaction.user.edit(nick=select.values[0])
        except Exception as e:
            print(e)
        await interaction.response.send_message(
            f"よくきたな{select.values[0]}\nさっさと"
            f"{discord.utils.get(interaction.guild.channels,name=select.values[0]).mention}"
            "に移動してロールを登録してくるんだな"
            )

class CharaSleMenuC2(discord.ui.View): # UIキットを利用するためにdiscord.ui.Viewを継承する
    def __init__(self): # Viewにはtimeoutがあり、初期値は180(s)である
        super().__init__(timeout=None)

    @discord.ui.select(
        cls=discord.ui.Select,
        placeholder="ネタバレ配慮　2（SUPER）",
        options=[
            discord.SelectOption(label="日向創"),
            discord.SelectOption(label="狛枝凪斗"),
            discord.SelectOption(label="田中眼蛇夢"),
            discord.SelectOption(label="左右田和一"),
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
        ],
        custom_id="chareslelessbare2"
    )
    async def select(self, interaction: discord.Interaction, select: discord.ui.Select):
        await interaction.user.add_roles(discord.utils.get(interaction.guild.roles, name=select.values[0]))
        gv.nick_to_data[select.values[0]].chara_ability=select.values[0]
        await interaction.user.add_roles(discord.utils.get(interaction.guild.roles, name="生存"))
        try:
            await interaction.user.edit(nick=select.values[0])
        except Exception as e:
            print(e)
        await interaction.response.send_message(
            f"よくきたな{select.values[0]}\nさっさと"
            f"{discord.utils.get(interaction.guild.channels,name=select.values[0]).mention}"
            "に移動してロールを登録してくるんだな"
            )

@bot.tree.command(name="monotaro",
                  description="キャラクターを選択し、Botに登録するメニューを出します",
                  guild=Test_GUILD
                  )
async def chara_select(itx:discord.Interaction):
    embedtxt = discord.Embed(
        title="キャラクター選択",
        description="おはっくまー！\nオマエはどちらから来た誰さん？\n\n（キャラカードを参照し、\n登場作品に対応したメニューからキャラクターを選択）"
        )

    await itx.response.send_message(embed=embedtxt,view=CharaSleMenuC1())
    await itx.followup.send(view=CharaSleMenuC2())
    await itx.followup.send(view=CharaSleMenu1())
    await itx.followup.send(view=CharaSleMenu2())

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
        await itx.user.add_roles(discord.utils.get(itx.guild.roles, name=select.values[0]))#しばらくは確認用に置いておく
        #データの格納
        gv.nick_to_data[itx.user.nick].role.name=select.values[0]
        gv.nick_to_data[itx.user.nick].role.id=role_name_to_para[select.values[0]]
        #登録済み人数のカウント
        gv.role_registered += 1
        #役職ごとのメンバーのリストに格納
        memlis={"シロ":gv.Cast.siro,"クロ":gv.Cast.kuro,"アルターエゴ":gv.Cast.alterego,
                "裏切者":gv.Cast.uragiri,"モノミ":gv.Cast.monomi,"超高校級の絶望":gv.Cast.tyozetsubo,
                "絶望病患者":gv.Cast.zetsubobyo,"ザコケモノ":gv.Cast.zako,
                "未来機関":gv.Cast.miraikikan,"絶望の残党":gv.Cast.zantou
                }
        memlis[select.values[0]].append(itx.user)
       #プレイヤー（キャラ紐づけデータが機能しているか確認用、そのうち消す）
        print(gv.nick_to_data[itx.user.nick])
        #登録内容の確認メッセージ投稿
        await itx.response.send_message("オマエニ、" + select.values[0] + " ノ、ロールヲ付与シマシタ", ephemeral=True)
        #全員の登録が終わったらクロと裏切者を各裏切者に通知
        if gv.role_registered == gv.player:
            uragiriyatura:str=""
            for uragirimono in gv.Cast.uragiri:
                uragiriyatura += uragirimono.nick+"\n"
            for uragirimono in gv.Cast.uragiri:
                await discord.utils.get(itx.guild.channels,name=uragirimono.nick).send(
                    f"クロは『{gv.Cast.kuro[0].nick}』です\n\n{uragiriyatura}は裏切者です"
                )

@bot.tree.command(name="monodam",description="役職登録メニューを出します",guild=Test_GUILD)
@commands.is_owner()
async def monodam(itx: discord.Interaction):
    await itx.response.send_message("ロール、ノ登録ヲ、オ願イスルヨ",view=RoleSleMenu())

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
        "Rehearsal",
        "Night",
        "Tsumiki",
        "KillrianCamera",
    ]
):
    await bot.reload_extension(f"cogs.{ext_name}")
    try:
        synced = await bot.tree.sync(guild=Test_GUILD)#コマンド同期しとかないとオートフィルでもうない変数要求されたりするので
        print(f"synced {len(synced)} commands ")
    except Exception as e:
        print(e)
    await itx.response.send_message(f"{ext_name}のリロードが完了しました",ephemeral=True)

bot.run(os.getenv("TOKEN"))