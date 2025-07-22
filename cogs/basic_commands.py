import discord
from discord import app_commands
from discord.ext import commands
from basic.time import timestamp

class BasicCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @app_commands.command(name="ping", description="봇과 디스코드 서버의 지연시간을 표시합니다.")
    async def ping(self, interaction: discord.Interaction):
        print("Log: " + timestamp + " /ping")
        latency = round(self.bot.latency * 1000)  # s -> ms
        await interaction.response.send_message(f"Pong! 🏓 지연시간: {latency}ms", ephemeral=True)

async def setup(bot):
    await bot.add_cog(BasicCommands(bot))