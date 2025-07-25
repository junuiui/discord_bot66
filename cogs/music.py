import discord 
from discord import app_commands
from discord.ext import commands
import nacl
from discord import FFmpegPCMAudio
import yt_dlp
import asyncio

class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.queue = []
    
    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{__name__} is online!")

    @app_commands.command(name="play", description="Play music from Youtube")
    @app_commands.describe(query="Search keyword or YouTube URL")
    async def play(self, interaction: discord.Interaction, query: str):
        print("/play called")
        
        # disabled
        await interaction.response.send_message("Sorry! The /play command is temporarily unavailable due to a technical issue.", ephemeral=True)
        return
        #####################
        
        if not interaction.user.voice or not interaction.user.voice.channel:
            await interaction.response.send_message("You are not in a voice channel", ephemeral=True)
            return

        voice_channel = interaction.user.voice.channel
        
        # Connect 
        vc = interaction.guild.voice_client
        if not vc:
            vc = await voice_channel.connect
        
        await interaction.response.send_message(f"Searching for `{query}`...", ephemeral=True)
        
        ytdlp_opts = {
            'format': 'bestaudio/best',
            'noplaylist': True,
            'quiet': True,
            'extract_flat': 'in_playlist',
            'default_search': 'ytsearch',
        }

        with yt_dlp.YoutubeDL(ytdlp_opts) as ydl:
            try:
                info = ydl.extract_info(query, download=False)
                if 'entries' in info:
                    info = info['entries'][0]  # First Search result

                url = info['url']
                title = info.get('title', 'Unknown Title')

                # 재생
                if not vc.is_playing():
                    ffmpeg_audio = FFmpegPCMAudio(info['url'], before_options="-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5")
                    vc.play(ffmpeg_audio)
                    await interaction.followup.send(f"Now playing: **{title}**")
                else:
                    await interaction.followup.send("Already playing audio. (Queue 기능은 아직 없음)")

            except Exception as e:
                await interaction.followup.send(f"Failed to play. Error: `{str(e)}`")
        
    # @app_commands.command(name="pause", description="")
    # async def pause(self, interaction: discord.Interaction):
    #     print("/pause called")
    #     # @TODO
        
    # @app_commands.command(name="skip", description="")
    # async def skip(self, interaction: discord.Interaction):
    #     print("/skip called")
    #     # @TODO
    
    # @app_commands.command(name="queue", description="")
    # async def queue(self, interaction: discord.Interaction):
    #     print("/queue called")
    #     # @TODO
        
async def setup(bot):
    await bot.add_cog(Music(bot))
