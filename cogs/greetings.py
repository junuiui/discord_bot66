import discord
from discord import app_commands
from discord.ext import commands
from discord.ui import View, Button

class Greetings(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # 슬래시 커맨드 (app_commands.command)
    @app_commands.command(name="hello", description="Say hello!")
    async def hello(self, interaction: discord.Interaction):
        await interaction.response.send_message("안녕하세요!", ephemeral=True)

    # 버튼 뷰 클래스
    class MyView(View):
        @discord.ui.button(label="클릭해봐", style=discord.ButtonStyle.primary)
        async def button_callback(self, button, interaction):
            await interaction.response.send_message("버튼 클릭됨!", ephemeral=True)

    @app_commands.command(name="button", description="버튼 테스트")
    async def button(self, interaction: discord.Interaction):
        await interaction.response.send_message("버튼을 눌러보세요!", view=self.MyView(), ephemeral=True)

async def setup(bot):
    await bot.add_cog(Greetings(bot))
