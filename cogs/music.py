import discord
from discord import app_commands
from discord.ext import commands
import yt_dlp
import asyncio

# /play
# /pause
# /resume
# /skip
# /queue
# /stop

# MY_GUILD_ID = 929204445705805836

class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.queue = {}  # guild_id : list of URLs

    async def search_youtube(self, query: str):
        ydl_opts = {
            'format': 'bestaudio/best',
            'noplaylist': True,
            'quiet': True,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            try:
                info = ydl.extract_info(f"ytsearch:{query}", download=False)['entries'][0]
                return info['url'], info['title']
            except Exception as e:
                print(f"Unable to find.. {e}")
                return None, None

    async def play_song(self, interaction: discord.Interaction, voice_client, url):
        source = await discord.FFmpegOpusAudio.from_probe(url, method='fallback')
        voice_client.play(source, after=lambda e: print(f"재생 오류: {e}") if e else None)

    @app_commands.command(name="play", description="노래 제목과 가수 이름으로 음악을 재생합니다.")
    async def play(self, interaction: discord.Interaction, *, query: str):
        await interaction.response.defer()

        voice = interaction.user.voice
        if not voice:
            await interaction.followup.send("음성 채널에 먼저 들어가 주세요.", ephemeral=True)
            return

        vc = interaction.guild.voice_client
        if not vc:
            vc = await voice.channel.connect()

        url, title = await self.search_youtube(query)
        if not url:
            await interaction.followup.send("노래를 찾을 수 없습니다.", ephemeral=True)
            return

        await interaction.followup.send(f"🎵 재생 중: **{title}**")

        await self.play_song(interaction, vc, url)

async def setup(bot):
    await bot.add_cog(Music(bot))
