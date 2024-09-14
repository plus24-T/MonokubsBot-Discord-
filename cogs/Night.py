import os

import discord
from discord import app_commands
from discord.ext import commands 
import discord.context_managers

from typing import List

import gv
import utils

#対象のセレクトメニュー及び朝時間開始時の処理
class Night_Select(discord.ui.Select):#1人選んでそれぞれの能力の対象にするため使用者で分岐させる
    def __init__(self,options:list[discord.SelectOption]):
        super().__init__(
            placeholder="対象を選択",
            options=options,
            disabled=False
            )
    #対象選択及び判別の各処理
    async def callback(self, itx: discord.Interaction):
        user_nickname = itx.user.nick
        user_role : gv.CharaRole = gv.get_chara_data(user_nickname).role
        #クロの処理
        if user_role == gv.CharaRole.KURO:
            gv.prog.remaining_processes -= 1
            osoware_yatsu=self.values[0]
            await itx.response.send_message(f"『{self.values[0]}』を襲撃することにしました")
        #モノミの処理
        elif user_role == gv.CharaRole.MONOMI:
            gv.prog.remaining_processes -= 1
            mamorare_yatsu=self.values[0]
            await itx.response.send_message(f"モノミと共に『{self.values[0]}』の部屋の前で夜通し見張ることにしました")
        #アルターエゴの処理
        elif user_role == gv.CharaRole.ALTEREGO:
            gv.prog.remaining_processes -= 1
            altered_yatsu=self.values[0]

            target_chara_name = altered_yatsu
            is_despair = utils.check_despair(itx, target_chara_name)
            if is_despair:
                await itx.response.send_message(f"『{target_chara_name}』は絶望〈ゼツボウ〉サイドです")
            else:
                await itx.response.send_message(f"『{target_chara_name}』は希望〈キボウ〉サイドです")
            
        #出揃ったあとの相互作用の確認及び朝時間突入の通知
        if gv.prog.remaining_processes == 0:#対象選択全部終わったら
            #残党の占死確認
            if gv.get_chara_data(altered_yatsu).role == gv.CharaRole.ZANTOU:
                cursed_killing:bool=True

            else:
                cursed_killing:bool=False
            #モノミの爆死確認、襲撃先の不在（占死済み）確認
            if cursed_killing:
                if osoware_yatsu==altered_yatsu:
                    absence:bool=True
                    exploded:bool=False
            else:
                if osoware_yatsu==mamorare_yatsu:
                    absence:bool=False
                    exploded:bool=True
                else:
                    absence:bool=False
                    exploded:bool=False
            #朝時間開始メッセージ
            gv.table_data.day_count+=1
            await discord.utils.get(itx.guild.channels,name="食堂").send(f"オハヨウゴザイマス\n{gv.table_data.day}日目の朝時間になりました")
            #残党占死メッセージおよび死亡ロール付与
            if cursed_killing:
                await discord.utils.get(itx.guild.channels,name="食堂").send(f"{altered_yatsu}の姿が見当たりませんね\n（アルターエゴの判別対象が絶望の残党だったため死亡しました）")
                gv.chara_role_list.zantou[0].remove_roles(discord.utils.get(itx.guild.roles,name="生存"))
                gv.chara_role_list.zantou[0].add_roles(discord.utils.get(itx.guild.roles,name="死亡"))
                #襲撃対象不在時（対象が残党で夜のうちに占死）メッセージ
            if absence:
                await discord.utils.get(itx.guild.channels,name="食堂").send("昨夜襲撃されたひとはいなかったようです\n（絶望の残党が襲撃先でした）")
            else:
                #襲撃先発表メッセージ
                await discord.utils.get(itx.guild.channels,name="食堂").send(f"{osoware_yatsu}が襲撃されました")
                #襲撃無効メッセージ
                if gv.get_chara_data(osoware_yatsu).escorted:
                    await discord.utils.get(itx.guild.channels,name="食堂").send(f"しかし{osoware_yatsu}には襲撃無効が付与されていたため\n襲撃は無効になりました")
                else:
                    #モノミ爆死メッセージおよび死亡ロール付与        
                    if exploded:
                        await discord.utils.get(itx.guild.channels,name="食堂").send(f"が！\n{gv.chara_role_list.monomi[0].nick}がモノミと共に身を挺して守ったため\n{osoware_yatsu}は助かりました\nしかし{gv.chara_role_list.monomi[0].nick}はモノミと共に爆死してしまったようです")
                        gv.chara_role_list.monomi[0].remove_roles(discord.utils.get(itx.guild.roles,name="生存"))
                        gv.table_data.kill_count+=1
                        gv.chara_role_list.monomi[0].add_roles(discord.utils.get(itx.guild.roles,name="死亡"))
            #襲撃無効効果リセット
            for member in discord.utils.get(itx.guild.roles,name="生存").members:
                gv.get_chara_data(member.nick).escorted=False

#選択対象渡しView       
class Night_View(discord.ui.View):
    def __init__(self,options:list[discord.SelectOption]):
        super().__init__(timeout=180)

        self.add_item(Night_Select(options=options))

#このコグのクラス化
class Night(commands.Cog):
    def __init__(self, bot:commands.Bot):
        self.bot = bot
    #夜時間処理呼び出しコマンド
    @app_commands.command(
            name="night",#coomand_nameがコマンドになる
            description="夜時間の役職能力（クロ、アルターエゴ、モノミ）を処理します"#コマンドリストに表示される説明文
            )
    async def night(self, itx:discord.Interaction):#ここが処理内容、必要な引数とか設定する
        #生存メンバーのリストから選択候補のリストを作成
        living_members = discord.utils.get(itx.guild.roles,name="生存").members
        select_op_living_members = []
        for member in living_members:
            select_op_living_members.append(discord.SelectOption(label=member.nick))
        #共通チャンネルに投稿
        await itx.response.send_message(f"{gv.table_data.day_count}日目の夜になりました\n夜が明けるまでしばらくお待ちください")
        #クロのプライベートチャンネルに投稿
        gv.prog.remaining_processes += 1 #後々アイテム効果で行なえない可能性があるのでちゃんと数えておく
        await discord.utils.get(itx.guild.channels,name=gv.chara_role_list.kuro[0].nick).send(
            "襲撃の対象を選択してください",
            view=Night_View(options=select_op_living_members)
            )
        #アルターエゴ(が生存しているなら)のプライベートチャンネルに投稿
        if gv.chara_role_list.alterego[0] in living_members:
                gv.prog.remaining_processes += 1
                await discord.utils.get(itx.guild.channels,name=gv.chara_role_list.alterego[0].nick).send(
                    "判別の対象を選択してください",
                    view=Night_View(options=select_op_living_members)
                    )
        #モノミ（が居て生存しているなら）のプライベートチャンネルに投稿
        if len(gv.chara_role_list.monomi)==1:
            if gv.chara_role_list.monomi[0] in living_members:
                gv.prog.remaining_processes += 1
                await discord.utils.get(itx.guild.channels,name=gv.chara_role_list.monomi[0].nick).send(
                    "護衛の対象を選択してください",
                    view=Night_View(options=select_op_living_members)
                    )
                
#エクステンションロード時のセットアップ
async def setup(bot:commands.Bot):
    await bot.add_cog(
        Night(bot),
        guilds = [discord.Object(id=bot.useGuildId)]
        )