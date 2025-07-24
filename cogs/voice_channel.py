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
        self.queue = []
    
    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{__name__} is online!")
        
    @app_commands.command(name="join", description="Joining the user's current vc")
    async def join(self, interaction: discord.Interaction):
        print("👉 /join called")
        
        await interaction.response.defer()  # ⏳ 응답 지연 선언

        if not interaction.user.voice:
            await interaction.followup.send("Error. You must be in the vc")
            return

        channel = interaction.user.voice.channel
        voice_client = interaction.guild.voice_client

        try:
            if voice_client is not None:
                if voice_client.channel == channel:
                    await interaction.followup.send(f"Already in **{channel}**!")
                    return
                else:
                    print("🔁 Moving to", channel)
                    await voice_client.move_to(channel)
            else:
                print("🎤 Connecting to", channel)
                await channel.connect()
            
            await interaction.followup.send(f"Joined **{channel}**!!")

        except Exception as e:
            print(f"❌ Failed to join VC. Error: {e}")
            await interaction.followup.send(f"❌ Failed to join VC. Error: {e}")

        
async def setup(bot):
    await bot.add_cog(Music(bot))

