import discord
from discord import app_commands
from discord.ext import commands

class BasicCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{__name__} is online!")
    
    @app_commands.command(name="ping", description="Latency Test")
    async def ping(self, interaction: discord.Interaction):
        latency = round(self.bot.latency * 1000)  # s -> ms
        await interaction.response.send_message(f"Latency: {latency}ms", ephemeral=True)

async def setup(bot):
    await bot.add_cog(BasicCommands(bot))