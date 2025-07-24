import discord
from discord import app_commands
from discord.ext import commands

class BasicCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{__name__} is online!")
        
    @app_commands.command(name="info", description="Show info about the bot and developer.")
    async def info(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="Azure (아쥬레) Bot Info",
            description="A Discord bot with utility, random, and music features.",
            color=discord.Color.blue()
        )
        embed.add_field(name="Pronunciation", value="Pronounced as **Ah-ZHU-ray (아쥬레)**", inline=False)
        embed.add_field(name="\u200b", value="―" * 40, inline=False)
        embed.add_field(name="Developer", value="Jun Hong", inline=False)
        embed.add_field(name="Technologies", value="Python, discord.py", inline=False)
        embed.add_field(name="GitHub", value="[GitHub Link](https://github.com/junuiui/discord_bot66)", inline=False)
        embed.add_field(name="\u200b", value="―" * 40, inline=False) 
        embed.set_footer(text="For a list of commands, use /help")
        
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="help", description="Show help information and command list.")
    async def help(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="Help Menu",
            description="Here's a list of available slash commands:",
            color=discord.Color.green()
        )

        embed.add_field(name="/info", value="Show info about the bot and developer.", inline=False)
        embed.add_field(name="/help", value="Show this help message.", inline=False)
        embed.add_field(name="/random_number min max", value="Get a random number in a given range.", inline=False)
        embed.add_field(name="/choose options", value="Choose one option from a comma-separated list.", inline=False)
        embed.add_field(name="/join", value="Join the voice channel you're in.", inline=False)
        embed.add_field(name="/leave", value="Leave the voice channel.", inline=False)
        embed.add_field(name="/play query", value="Search and play music from YouTube.", inline=False)

        await interaction.response.send_message(embed=embed)
    
    @app_commands.command(name="ping", description="Latency Test")
    async def ping(self, interaction: discord.Interaction):
        latency = round(self.bot.latency * 1000)  # s -> ms
        await interaction.response.send_message(f"Latency: {latency}ms", ephemeral=True)

async def setup(bot):
    await bot.add_cog(BasicCommands(bot))