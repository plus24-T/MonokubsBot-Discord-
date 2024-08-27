import os 
import discord.context_managers
from dotenv import load_dotenv

import discord
from discord import app_commands
from discord.ext import commands

load_dotenv()

class Ext_test(commands.Cog):
    def __init__(self, bot:commands.Bot):
        self.bot = bot

    @app_commands.command(
            name="ext_test",
            description="エクステンションのテスト奴"
            )
    async def ext_test(self, itx:discord.Interaction):
        await itx.response.send_message("TEST!")

async def setup(bot:commands.Bot):
    await bot.add_cog(
        Ext_test(bot),
        guilds = [discord.Object(id=os.getenv("GUILD_ID"))]
        )
