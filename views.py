import discord
from discord.ext import commands

import gv

# あちこちで使う discord.ui 系の処理をここに記載する
# utilsから使う定義などもここ

# 役職ロールセレクトメニュー
class RoleSleMenu(discord.ui.View):
    def __init__(self, bot : commands.Bot):
        super().__init__(timeout=None)
        self.bot = bot

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
        #データの格納
        userNickName = itx.user.nick
        gv.get_chara_data(userNickName).role = gv.CharaRole.parse(select.values[0]) 
        #登録済み人数のカウント
        gv.prog.role_registered += 1
        #役職ごとのメンバーのリストに格納
        memlis={"シロ":gv.chara_role_list.siro,"クロ":gv.chara_role_list.kuro,"アルターエゴ":gv.chara_role_list.alterego,
                "裏切者":gv.chara_role_list.uragiri,"モノミ":gv.chara_role_list.monomi,"超高校級の絶望":gv.chara_role_list.tyozetsubo,
                "絶望病患者":gv.chara_role_list.zetsubobyo,"ザコケモノ":gv.chara_role_list.zako,
                "未来機関":gv.chara_role_list.miraikikan,"絶望の残党":gv.chara_role_list.zantou
                }
        memlis[select.values[0]].append(itx.user)
       #プレイヤー（キャラ紐づけデータが機能しているか確認用、そのうち消す）
        print(gv.get_chara_data(userNickName))
        #登録内容の確認メッセージ投稿
        await itx.response.send_message("オマエハ、" + select.values[0] + " ダナ、了解シタ")
        #裏切者以外を食堂（共通チャンネル）へ誘導
        if gv.get_chara_data(userNickName).role != gv.CharaRole.URAGIRI:
            await itx.followup.send(
                f"{discord.utils.get(itx.guild.channels,name="食堂").mention}"
                "へ移動して、しばらくお待ちください。"
                )
        #全員の登録が終わったらクロと裏切者を各裏切者に通知
        if gv.prog.role_registered == gv.table_data.player_count:
            if len(gv.chara_role_list.uragiri)==0:#裏切者欠け（居ない）時の処理
                discord.utils.get(itx.guild.channels,name="食堂").send(
                    "0日目の昼です、皆様、しばし御歓談ください\n"
                    "（キャラ能力説明等を行ってください\n"
                    "【夜時間を開始する】ボタンで夜時間が始まります）",
                    view=Night0(self.bot)
                    )
            else:
                uragiriyatura:str=""
                for uragirimono in gv.chara_role_list.uragiri:
                    uragiriyatura += uragirimono.nick+"\n"
                for uragirimono in gv.chara_role_list.uragiri:
                    gv.prog.ok_mati+=1
                    await discord.utils.get(itx.guild.channels,name=uragirimono.nick).send(
                        f"クロは『{gv.chara_role_list.kuro[0].nick}』です\n\n{uragiriyatura}は裏切者です"
                        "\n\nクロと裏切者が誰か読み終わったらOKを押して下さい",
                        view=OK_Button(self.bot)
                        )


#OKボタン（裏切者の開始時情報確認待ち）→0日目昼へ
class OK_Button(discord.ui.View):
    def __init__(self, bot : commands.Bot):
        super().__init__(timeout=None)
        self.bot = bot

    @discord.ui.button(
        label="OK",
        disabled=False,
        style=discord.ButtonStyle.success
    )
    async def ok(self,button:discord.ui.Button,interaction:discord.Interaction):
        gv.prog.ok_mati-=1
        self.disabled=True
        await interaction.response.send_message(
            "確認しました、"
            f"{discord.utils.get(interaction.guild.channels,name="食堂").mention}"
            "へ移動し、しばらくお待ちください")
        if gv.prog.ok_mati==0:
            discord.utils.get(interaction.guild.channels,name="食堂").send(
                "0日目の昼です、皆様、しばし御歓談ください\n"
                "（キャラ能力説明等を行ってください\n"
                "【夜時間を開始する】ボタンで夜時間が始まります）",
                view=Night0(self.bot)
                )
            
#0日目夜時間（下見）開始ボタン
class Night0(discord.ui.View):
    def __init__(self, bot : commands.Bot):
        super().__init__(timeout=None)
        self.bot = bot

    @discord.ui.button(
        label="夜時間を開始する",
        disabled=False,
        style=discord.ButtonStyle.danger
    )
    async def start_night0(self,button:discord.ui.Button,interaction:discord.Interaction):
        await interaction.response.send_message("")#インタラクションに失敗しました（赤い字）の表示を阻止
        #コマンド呼び出し
        ctx = await self.bot.get_context(interaction.message)
        ctx.command = self.bot.get_command("rehearsal")#ここでコマンドを指定
        await self.bot.invoke(ctx)



#下見処理（アイテム一枚捨てる）終了確認ボタン
class RehearsalEndConfirmationButton(discord.ui.View):
    def __init__(self, bot : commands.Bot):
        super().__init__(timeout=None)
        self.bot = bot

    @discord.ui.button(
        label="捨てました",
        disabled=False,
        style=discord.ButtonStyle.grey
    )
    async def item_discarded(self,button:discord.ui.Button,interaction:discord.Interaction):
        button.style = discord.ButtonStyle.success
        button.disabled=True
        await interaction.response.send_message("確認しました、"
                f"{discord.utils.get(interaction.guild.channels,name="食堂").mention}"
                "へお戻りください"    
                )
        discord.utils.get(interaction.guild.channels,name="食堂").send(
                "1日目の昼時間が始まりました、昼時間のアイテムや能力使用を全て確認したあと\n"
                "ブリーフィングタイム（3分間）を行ってください\n"
                "【夜時間を開始する】ボタンで夜時間が始まります）",
                view=NightStartButton(self.bot)
                )
        

 #夜時間開始ボタン
class NightStartButton(discord.ui.View):
    def __init__(self, bot : commands.Bot):
        super().__init__(timeout=None)
        self.bot = bot

    @discord.ui.button(
        label="夜時間を開始する",
        disabled=False,
        style=discord.ButtonStyle.grey
    )
    async def night_start(self,button:discord.ui.Button,interaction:discord.Interaction):
        button.style = discord.ButtonStyle.success
        button.disabled=True
        await interaction.response.send_message(
            f"{gv.table_data.day_count}日目の夜時間が始まりました、"
            "夜時間のアイテムや能力使用をすべて確認したあと"            
            "【おやすみなさい】ボタンを押してください"
            "(クロの襲撃、アルターエゴの判別、モノミの護衛の対象の指定ののち、朝時間が始まります)",
            view=GoodNightButton(self.bot)
            )
        await interaction.followup.send(
            "判別能力を使用するときはこのボタンを押してください",
            view=NightIdentificationAbilitiesButton(self.bot)
        )
        await interaction.followup.send(
            "判別系アイテムを使用するときはこのボタンを押してください",
            view=NightIdentificationItemsButton(self.bot)
        )


#夜時間の役職能力処理開始ボタン（おやすみなさいボタン）
class GoodNightButton(discord.ui.View):
    def __init__(self, bot : commands.Bot):
        super().__init__(timeout=None)
        self.bot = bot

    @discord.ui.button(
        label="おやすみなさい",
        disabled=False,
        style=discord.ButtonStyle.danger
    )
    async def night_start(self,button:discord.ui.Button,interaction:discord.Interaction):
        button.style = discord.ButtonStyle.gray
        button.disabled=True
        await interaction.response.send_message("")#赤文字回避
        ctx = await self.bot.get_context(interaction.message)
        ctx.command = self.bot.get_command('night')
        await self.bot.invoke(ctx)


#夜時間の判別キャラクター能力使用ボタン
class NightIdentificationAbilitiesButton(discord.ui.View):
    def __init__(self, bot : commands.Bot):
        super().__init__(timeout=None)
        self.bot = bot

    @discord.ui.button(
        label="霧切響子"
    )
    async def use_kirigiri_ability(self, button: discord.ui.Button, interaction: discord.Interaction):
        await interaction.response.send_message("")#インタラクションに失敗しました（赤い字）の表示を阻止
        # ボタンを押したメンバーのコンテキストを作成
        ctx = await self.bot.get_context(interaction.message)
        ctx.author = interaction.user
        ctx.command = self.bot.get_command('kirigiri')
        await self.bot.invoke(ctx)

    @discord.ui.button(
        label="葉隠康比呂"
    )
    async def use_hagakure_ability(self, button: discord.ui.Button, interaction: discord.Interaction):
        await interaction.response.send_message("")#インタラクションに失敗しました（赤い字）の表示を阻止
        # ボタンを押したメンバーのコンテキストを作成
        ctx = await self.bot.get_context(interaction.message)
        ctx.author = interaction.user
        ctx.command = self.bot.get_command('hagakure')
        await self.bot.invoke(ctx)


#夜時間の判別アイテム使用ボタン
class NightIdentificationItemsButton(discord.ui.View):
    def __init__(self, bot : commands.Bot):
        super().__init__(timeout=None)
        self.bot = bot

    @discord.ui.button(
        label="無言電話"
    )
    async def use_silent_phone(self, button: discord.ui.Button, interaction: discord.Interaction):
        await interaction.response.send_message("")#インタラクションに失敗しました（赤い字）の表示を阻止
        # ボタンを押したメンバーのコンテキストを作成
        ctx = await self.bot.get_context(interaction.message)
        ctx.author = interaction.user
        ctx.command = self.bot.get_command('silent_phone')
        await self.bot.invoke(ctx)

    @discord.ui.button(
        label="誰かの卒業アルバム"
    )
    async def use_silent_phone(self, button: discord.ui.Button, interaction: discord.Interaction):
        await interaction.response.send_message("")#インタラクションに失敗しました（赤い字）の表示を阻止
        # ボタンを押したメンバーのコンテキストを作成
        ctx = await self.bot.get_context(interaction.message)
        ctx.author = interaction.user
        ctx.command = self.bot.get_command('album')
        await self.bot.invoke(ctx)

    @discord.ui.button(
        label="おでこのメガネ"
    )
    async def use_silent_phone(self, button: discord.ui.Button, interaction: discord.Interaction):
        await interaction.response.send_message("")#インタラクションに失敗しました（赤い字）の表示を阻止
        # ボタンを押したメンバーのコンテキストを作成
        ctx = await self.bot.get_context(interaction.message)
        ctx.author = interaction.user
        ctx.command = self.bot.get_command('megane')
        await self.bot.invoke(ctx)


#夜時間の護衛アイテム使用ボタン
class NightEscortItemsButton(discord.ui.View):
    def __init__(self, bot : commands.Bot):
        super().__init__(timeout=None)
        self.bot = bot

    @discord.ui.button(
        label="黄金銃"
    )
    async def golden_gun(self, button: discord.ui.Button, interaction: discord.Interaction):
        gv.get_chara_data(interaction.user.nick).escorted=True
        await interaction.response.send_message(f"{interaction.user.nick}が黄金銃を使用しました\n今夜{interaction.user.nick}への襲撃は無効になります")

    @discord.ui.button(
        label="ジャスティスロボ"
    )
    async def justice_robot(self, button: discord.ui.Button, interaction: discord.Interaction):
        #生存メンバーのリストから選択候補のリストを作成
        living_members = discord.utils.get(interaction.guild.roles,name="生存").members
        select_op_living_members = []
        for member in living_members:
            select_op_living_members.append(discord.SelectOption(label=member.nick))
        user_channel = discord.utils.get(interaction.guild.channels,name=interaction.user.nick)
        await interaction.response.send_message(
            f"{user_channel.mention}に移動して護衛対象を選択してください"
        )
        user_channel.send(
            "ジャスティスロボの護衛対象を選択してください",
            view=JusticeRobot_View(options=select_op_living_members))
        
class JusticeRobot_Select(discord.ui.Select):
    def __init__(self,options:list[discord.SelectOption]):
        super().__init__(
            placeholder="対象を選択",
            options=options,
            disabled=False
            )
    async def callback(self, interaction: discord.Interaction):
        target_name = self.values[0]
        gv.get_chara_data(target_name).escorted = True
        await interaction.response.send_message(f"{target_name}を護衛対象に選択しました")
        discord.utils.get(interaction.guild.channels,name="食堂").send(
            f"{target_name}が護衛対象に選択されました"
        )
  
class JusticeRobot_View(discord.ui.View):
    def __init__(self, bot : commands.Bot, options:list[discord.SelectOption]):
        super().__init__(timeout=None)
        self.bot = bot
        self.add_item(JusticeRobot_Select(options=options))
