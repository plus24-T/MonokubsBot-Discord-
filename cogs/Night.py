import os
from dotenv import load_dotenv

import discord
from discord import app_commands
from discord.ext import commands 
import discord.context_managers

from typing import List

import gv

load_dotenv()

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
        #クロの処理
        if gv.nick_to_data[itx.user.nick].role.name=="クロ":
            gv.remaining_processes -= 1
            osoware_yatsu=self.values[0]
            await itx.response.send_message(f"『{self.values[0]}』を襲撃することにしました")
        #モノミの処理
        elif gv.nick_to_data[itx.user.nick].role.name=="モノミ":
            gv.remaining_processes -= 1
            mamorare_yatsu=self.values[0]
            await itx.response.send_message(f"モノミと共に『{self.values[0]}』の部屋の前で夜通し見張ることにしました")
        #アルターエゴの処理
        elif gv.nick_to_data[itx.user.nick].role.name=="アルターエゴ":
            gv.remaining_processes -= 1
            altered_yatsu=self.values[0]
            if len(discord.utils.get(itx.guild.roles,name="死亡").members)==0:
                despair_threshold=3
            else:
                despair_threshold=2

            if gv.nick_to_data[self.values[0]].role.id <=despair_threshold:
                await itx.response.send_message(f"『{self.values[0]}』は希望〈キボウ〉サイドです")
            else:
                if gv.nick_to_data[self.values[0]].role.id != 6:
                    await itx.response.send_message(f"『{self.values[0]}』は絶望〈ゼツボウ〉サイドです")
                else:
                    if len(gv.Cast.zantou)==0:
                        await itx.response.send_message(f"『{self.values[0]}』は絶望〈ゼツボウ〉サイドです")
                    else:
                        if gv.Cast.zantou[0] in discord.utils.get(itx.guild.roles,name="死亡").members:
                            await itx.response.send_message(f"『{self.values[0]}』は絶望〈ゼツボウ〉サイドです")
                        else:
                            await itx.response.send_message(f"『{self.values[0]}』は希望〈キボウ〉サイドです")
        #出揃ったあとの相互作用の確認及び朝時間突入の通知
        if gv.remaining_processes == 0:#対象選択全部終わったら
            #残党の占死確認
            if gv.nick_to_data[altered_yatsu].role.name=="絶望の残党":
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
        await discord.utils.get(itx.guild.channels,name="食堂").send(f"オハヨウゴザイマス\nn日目の朝時間になりました")
        #残党占死メッセージおよび死亡ロール付与
        if cursed_killing:
            await discord.utils.get(itx.guild.channels,name="食堂").send(f"{altered_yatsu}の姿が見当たりませんね\n（アルターエゴの判別対象が絶望の残党だったため死亡しました）")
            gv.Cast.zantou[0].remove_roles(discord.utils.get(itx.guild.roles,name="生存"))
            gv.Cast.zantou[0].add_roles(discord.utils.get(itx.guild.roles,name="死亡"))
            #襲撃対象不在時（対象が残党で夜のうちに占死）メッセージ
            if absence:
                await discord.utils.get(itx.guild.channels,name="食堂").send("昨夜襲撃されたひとはいなかったようです\n（絶望の残党が襲撃先でした）")
                pass
        #襲撃先発表メッセージ
        await discord.utils.get(itx.guild.channels,name="食堂").send(f"{osoware_yatsu}が襲撃されました")
        #モノミ爆死メッセージおよび死亡ロール付与        
        if exploded:
            await discord.utils.get(itx.guild.channels,name="食堂").send(f"が！\n{gv.Cast.monomi[0].nick}がモノミと共に身を挺して守ったため\n{osoware_yatsu}は助かりました\nしかし{gv.Cast.monomi[0].nick}はモノミと共に爆死してしまったようです")
            gv.Cast.monomi[0].remove_roles(discord.utils.get(itx.guild.roles,name="生存"))
            gv.kill+=1
            gv.Cast.monomi[0].add_roles(discord.utils.get(itx.guild.roles,name="死亡"))
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
        await itx.response.send_message("ｎ日目の夜です\n夜が明けるまでしばらくお待ちください")
        #クロのプライベートチャンネルに投稿
        gv.remaining_processes += 1 #後々アイテム効果で行なえない可能性があるのでちゃんと数えておく
        await discord.utils.get(itx.guild.channels,name=gv.Cast.kuro[0].nick).send(
            "襲撃の対象を選択してください",
            view=Night_View(options=select_op_living_members)
            )
        #アルターエゴ(が生存しているなら)のプライベートチャンネルに投稿
        if gv.Cast.alterego[0] in living_members:
                gv.remaining_processes += 1
                await discord.utils.get(itx.guild.channels,name=gv.Cast.alterego[0].nick).send(
                    "判別の対象を選択してください",
                    view=Night_View(options=select_op_living_members)
                    )
        #モノミ（が居て生存しているなら）のプライベートチャンネルに投稿
        if len(gv.Cast.monomi)==1:
            if gv.Cast.monomi[0] in living_members:
                gv.remaining_processes += 1
                await discord.utils.get(itx.guild.channels,name=gv.Cast.monomi[0].nick).send(
                    "護衛の対象を選択してください",
                    view=Night_View(options=select_op_living_members)
                    )
#エクステンションロード時のセットアップ
async def setup(bot:commands.Bot):
    await bot.add_cog(
        Night(bot),
        guilds = [discord.Object(id=os.getenv("GUILD_ID"))]
        )