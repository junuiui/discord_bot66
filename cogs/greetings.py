import discord
from discord import app_commands
from discord.ext import commands


class Greetings(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{__name__} is online!")

    @app_commands.command(name="hello", description="Say hello!")
    async def hello(self, interaction: discord.Interaction):
        await interaction.response.send_message(f'Hi, {interaction.user.display_name}!', ephemeral=True)

async def setup(bot):
    await bot.add_cog(Greetings(bot))
