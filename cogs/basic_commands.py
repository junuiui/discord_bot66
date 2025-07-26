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
            title="`Azure` (아쥬레) Bot Info",
            description="A Discord bot with utility (planner included), random, and music features.",
            color=discord.Color.blue()
        )
        embed.add_field(name="How to say?", value="Pronounced as **Ah-ZHU-ray (아쥬레)**", inline=False)
        embed.add_field(name="\u200b", value="―" * 10, inline=False)
        embed.add_field(name="Developer", value="`Jun Hong`", inline=False)
        embed.add_field(name="Technologies", value="`Python`, `discord.py`, `OPENAI API`, `PyNaCl`, `yt_dlp`", inline=False)
        embed.add_field(name="GitHub", value="[`GitHub Link`](https://github.com/junuiui/discord_bot66)", inline=False)
        embed.add_field(name="How to reach me", value="DM `junuiui`", inline=False)
        embed.add_field(name="\u200b", value="―" * 10, inline=False) 
        embed.set_footer(text="For a list of commands, use /help")
        
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="help", description="Show commands.")
    async def help(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="Help Menu",
            description="Here's a list of available and unavailable slash commands:",
            color=discord.Color.green()
        )

        # Available commands
        embed.add_field(name="\u200b", value="―" * 10, inline=False)
        embed.add_field(name="**Available Commands**", value="\u200b", inline=False)
        embed.add_field(name="`/hello`", value="Say hello to Azure!", inline=True)
        embed.add_field(name="`/info`", value="Show info about the bot and developer.", inline=False)
        embed.add_field(name="`/help`", value="Show this help message.", inline=False)
        embed.add_field(name="`/ping`", value="Check the bot's response time (latency).", inline=False)

        # divide sections
        embed.add_field(name="\u200b", value="\u200b", inline=False)
        embed.add_field(name="`/random_number`", value="Get a random number in a given range.", inline=False)
        embed.add_field(name="`/choose`", value="Choose one option from a comma-separated list.", inline=False)
        embed.add_field(name="`/flip_coin`", value="Flip a coin (Heads or Tails).", inline=False)
        embed.add_field(name="`/shuffle`", value="Shuffle a comma-separated list of items.", inline=False)
        embed.add_field(name="`/8ball`", value="Ask the magic 8-ball a yes/no question.", inline=False)
        embed.add_field(name="`/random_date`", value="Get a random date between two dates.", inline=False)
        embed.add_field(name="`/roll_dice`", value="Roll a dice (d6, d20, etc.).", inline=False)

        embed.add_field(name="\u200b", value="\u200b", inline=False)
        embed.add_field(name="`/plan_add`", value="Add a new plan or task with a title and optional note.", inline=False)
        embed.add_field(name="`/plan_list`", value="List all your saved plans or tasks.", inline=False)
        embed.add_field(name="`/plan_delete`", value="Delete a saved plan by ID.", inline=False)
        embed.add_field(name="`/plan_latest`", value="Show the most recent plan you added.", inline=False)

        # Unavailable commands
        embed.add_field(name="\u200b", value="―" * 10, inline=False)
        embed.add_field(name="**Unavailable Commands (temporarily disabled)**", value="\u200b", inline=False)
        embed.add_field(name="`/join`", value="(NOT WORKING) Join the voice channel you're in.", inline=False)
        embed.add_field(name="`/leave`", value="(NOT WORKING) Leave the voice channel.", inline=False)
        embed.add_field(name="`/ask`", value="(NOT WORKING) Ask AI a question and get a response.", inline=False)
        embed.add_field(name="`/pause`", value="(NOT WORKING) Pause the current music track.", inline=False)
        embed.add_field(name="`/play`", value="(NOT WORKING) Search and play music from YouTube.", inline=False)
        embed.add_field(name="`/queue`", value="(NOT WORKING) Show the current music queue.", inline=False)

        await interaction.response.send_message(embed=embed)


    
    @app_commands.command(name="ping", description="Latency Test")
    async def ping(self, interaction: discord.Interaction):
        latency = round(self.bot.latency * 1000)  # s -> ms
        await interaction.response.send_message(f"Latency: {latency}ms", ephemeral=True)

async def setup(bot):
    await bot.add_cog(BasicCommands(bot))