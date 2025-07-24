import discord 
from discord import app_commands
from discord.ext import commands
# from discord import FFmpegPCMAudio
# import yt_dlp
# import asyncio

class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.queue = []
        
    # @app_commands.command(name="join", description="Joining the user's current vc")
    # async def join(self, interaction: discord.Interaction):
    #     if not interaction.user.voice:
    #         await interaction.response.send_message("Error. You must be in the vc")
    #         return

    #     channel = interaction.user.voice.channel
    #     if interaction.guild.voice_client is not None:
    #         await interaction.guild.voice_client.move_to(channel)
    #     else:
    #         await channel.connect()

    #     await interaction.response.send_message(f"Joined **{channel}**!!")

        
async def setup(bot):
    await bot.add_cog(Music(bot))

