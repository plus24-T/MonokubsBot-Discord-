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
        await itx.response.send_message("オマエハ、" + select.values[0] + " 了解シタ")
        #全員の登録が終わったらクロと裏切者を各裏切者に通知
        if gv.prog.role_registered == gv.table_data.player:
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
        await interaction.response.defer()
        #コマンド呼び出し
        ctx = await self.bot.get_context(interaction.message)
        ctx.command = self.bot.get_command("rehearsal")#ここでコマンドを指定
        await self.bot.invoke(ctx)


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
        await interaction.response.send_message("確認しました、しばらくお待ちください")
        if gv.prog.ok_mati==0:
            discord.utils.get(interaction.guild.channels,name="食堂").send(
                "0日目の昼です、皆様、しばし御歓談ください\n"
                "（キャラ能力説明等を行ってください\n"
                "【夜時間を開始する】ボタンで夜時間が始まります）",
                view=Night0(self.bot)
                )
