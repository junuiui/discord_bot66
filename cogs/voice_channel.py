import discord 
from discord import app_commands
from discord.ext import commands
import nacl
# from discord import FFmpegPCMAudio
# import yt_dlp
# import asyncio

class Voice_Channel(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{__name__} is online!")
        
    @app_commands.command(name="join", description="Joining the user's current vc")
    async def join(self, interaction: discord.Interaction):
        print("/join called")
        
        # disabled
        await interaction.response.send_message("Sorry! The /join command is temporarily unavailable due to a technical issue. Try /help to see what’s available!", ephemeral=True)
        return
        #####################

        vc = interaction.user.voice
        
        # Check user's vc status
        if not vc or not vc.channel:
            await interaction.response.send_message("You are not in a voice channel. Make sure you are in the voice channel", ephemeral=True)
            return

        channel = vc.channel
        await interaction.response.send_message(f"Connecting to **{channel.name}**...", ephemeral=True)
        try:
            await channel.connect()
            await interaction.followup.send(f"Successfully connected to **{channel.name}**", ephemeral=True)
        except discord.ClientException:
            await interaction.followup.send(f"Already connected to **{channel.name}**", ephemeral=True)
        except Exception as e:
            await interaction.followup.send(f"Failed to join VC. Error: **{str(e)}**", ephemeral=True)
        
    @app_commands.command(name="leave", description="Leave the voice channel")
    async def leave(self, interaction: discord.Interaction):
        vc = interaction.guild.voice_client

        if not vc or not vc.is_connected():
            await interaction.response.send_message("I'm not connected to any voice channel. Try /help to see what’s available!", ephemeral=True)
            return

        channel = vc.channel
        await vc.disconnect()
        await interaction.response.send_message(f"Disconnected from **{channel.name}**.", ephemeral=True)
        
async def setup(bot):
    await bot.add_cog(Voice_Channel(bot))

