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
        
    async def play_next(self):
        if len(self.queue) == 0:
            self.is_playing = False
            return

        title, url, interaction = self.queue.pop(0)
        self.is_playing = True
        ffmpeg_audio = FFmpegPCMAudio(url, before_options="-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5")

        if self.vc:
            self.vc.play(ffmpeg_audio, after=lambda e: asyncio.run_coroutine_threadsafe(self.play_next(), self.bot.loop))

            try:
                await interaction.followup.send(f"Now playing: **{title}**")
            except:
                pass 

    @app_commands.command(name="play", description="Play music from Youtube")
    @app_commands.describe(query="Search keyword or YouTube URL")
    async def play(self, interaction: discord.Interaction, query: str):
        print("/play called")
        
        # disabled
        await interaction.response.send_message("Sorry! The /play command is temporarily unavailable due to a technical issue. Try /help to see what’s available!", ephemeral=True)
        return
        #####################
        
        await interaction.response.defer(thinking=True)

        if not interaction.user.voice or not interaction.user.voice.channel:
            await interaction.followup.send("You are not in a voice channel.", ephemeral=True)
            return

        if not self.vc or not self.vc.is_connected():
            self.vc = await interaction.user.voice.channel.connect()

        ytdlp_opts = {
            'format': 'bestaudio/best',
            'noplaylist': True,
            'quiet': True,
            'default_search': 'ytsearch',
        }

        with yt_dlp.YoutubeDL(ytdlp_opts) as ydl:
            try:
                info = ydl.extract_info(query, download=False)
                if 'entries' in info:
                    info = info['entries'][0]

                url = info['url']
                title = info.get('title', 'Unknown Title')

                self.queue.append((title, url, interaction))

                if not self.is_playing:
                    await self.play_next()
                else:
                    await interaction.followup.send(f"Queued: **{title}**")

            except Exception as e:
                await interaction.followup.send(f"Error: `{str(e)}`")
        
    @app_commands.command(name="pause", description="Pause the current music")
    async def pause(self, interaction: discord.Interaction):
        print("/pause called")

        # Disabled
        await interaction.response.send_message("Sorry! The /pause command is temporarily unavailable due to a technical issue. Try /help to see what’s available!", ephemeral=True)
        return

        if self.vc and self.vc.is_playing():
            self.vc.pause()
            await interaction.response.send_message("Playback paused.")
        else:
            await interaction.response.send_message("Nothing is playing.", ephemeral=True)

    @app_commands.command(name="skip", description="Skip the current music")
    async def skip(self, interaction: discord.Interaction):
        print("/skip called")

        # Disabled
        await interaction.response.send_message("Sorry! The /skip command is temporarily unavailable due to a technical issue. Try /help to see what’s available!", ephemeral=True)
        return

        if self.vc and self.vc.is_playing():
            self.vc.stop()
            await interaction.response.send_message("Song skipped.")
        else:
            await interaction.response.send_message("Nothing is playing.", ephemeral=True)

    @app_commands.command(name="queue", description="Show the upcoming songs in queue")
    async def queue_cmd(self, interaction: discord.Interaction):
        print("/queue called")

        # Disabled
        await interaction.response.send_message("Sorry! The /queue command is temporarily unavailable due to a technical issue. Try /help to see what’s available!", ephemeral=True)
        return

        if len(self.queue) == 0:
            await interaction.response.send_message("The queue is empty.")
        else:
            queue_list = '\n'.join([f"{idx+1}. {title}" for idx, (title, _, _) in enumerate(self.queue)])
            await interaction.response.send_message(f"**Current Queue:**\n{queue_list}")
        
async def setup(bot):
    await bot.add_cog(Music(bot))
