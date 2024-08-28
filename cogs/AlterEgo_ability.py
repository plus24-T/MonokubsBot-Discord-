import os 
import discord.context_managers
from dotenv import load_dotenv
import translation
import discord
from discord import app_commands
from discord.ext import commands

load_dotenv()

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
          
        if nick_to_data[self.values[0]].role.id <=despair_threshold:
            await itx.response.send_message(f"『{self.values[0]}』は希望〈キボウ〉サイドです")
        else:
            if nick_to_data[self.values[0]].role.id != 6:
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
