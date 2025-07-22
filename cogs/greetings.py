import discord
from discord import app_commands
from discord.ext import commands
from discord.ui import View, Button
from basic.time import timestamp


class Greetings(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="hello", description="Say hello!")
    async def hello(self, interaction: discord.Interaction):
        print("Log: " + timestamp() + " /hello")
        await interaction.response.send_message(f'Hi, {interaction.user.display_name}!', ephemeral=True)

async def setup(bot):
    await bot.add_cog(Greetings(bot))
