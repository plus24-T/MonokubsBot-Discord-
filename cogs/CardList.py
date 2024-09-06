import os 
import discord.context_managers
from dotenv import load_dotenv

import discord
from discord import app_commands
from discord.ext import commands
from discord.ext.ui import View,ViewTracker, MessageProvider,PageView,PaginationView,Message

load_dotenv()
#試作中　動かないよ！


class Page(PageView):
    def __init__(self, content: str):
        super(Page, self).__init__()
        self.content = content

    async def body(self) -> Message | View:
        return  Message(self.content)

    async def on_appear(self, paginator: PaginationView) -> None:
        print(f"appeared page: {paginator.page}")

class CardList(commands.Cog):
    def __init__(self, bot:commands.Bot):
        self.bot = bot

    @app_commands.command(
            name="card_list",#comand_nameがコマンドになる
            description="ページ送り型のカードリスト出す奴"#コマンドリストに表示される説明文
            )
    async def card_list(self, itx:discord.Interaction):#ここが処理内容、必要な引数とか設定する
        view = Page([
            Page("The first page -- Morning --"),
            Page("The second page -- Noon --"),
            Page("The third page -- Afternoon --"),
            Page("The forth page -- Evening --"),
            Page("The last page -- Good night! --"),
        ])
        tracker = ViewTracker(view, timeout=None)
        await tracker.track(MessageProvider(itx.channel))

async def setup(bot:commands.Bot):
    await bot.add_cog(
        CardList(bot),
        guilds = [discord.Object(id=os.getenv("GUILD_ID"))]
        )
