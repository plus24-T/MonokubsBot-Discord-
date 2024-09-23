import os 
import discord.context_managers

import discord
from discord import app_commands
from discord.ext import commands


class Ext_test(commands.Cog):
    def __init__(self, bot:commands.Bot):
        self.bot = bot

    @app_commands.command(
            name="ext_test",
            description="エクステンションのテスト奴"
            )
    async def ext_test(self, interaction:discord.Interaction):
        await interaction.response.send_message("TEST!")

async def setup(bot:commands.Bot):
    await bot.add_cog(
        Ext_test(bot),
        guilds = [discord.Object(id=bot.useGuildId)]
        )
