import discord 
from discord import app_commands
from discord.ext import commands
import random

class Games(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @app_commands.command(name="random_number", description="Get the random number")
    @app_commands.describe(start="Start of the range", end="End of the range")
    async def random_number(self, interaction: discord.Interaction, start: int, end: int):
        if start > end:
            await interaction.response.send_message("Start must be less than or equal to End.", ephemeral=True)
            return
        number = random.randint(start, end)
        await interaction.response.send_message(f"Random number between `{start}` and `{end}`: **{number}**")
        
    @app_commands.command(name="choose", description="Choose one from the given options")
    @app_commands.describe(options="Type options separated by commas (e.g. A, B, C)")
    async def choose(self, interaction: discord.Interaction, options: str):
        items = [item.strip() for item in options.split(",") if item.strip()]
        if len(items) < 2:
            await interaction.response.send_message("Please enter at least two options, separated by commas.", ephemeral=True)
            return
        choice = random.choice(items)
        await interaction.response.send_message(f"Result: **{choice}**")
        
    @app_commands.command(name="roll_dice", description="Roll a dice")
    @app_commands.describe(sides="Number of sides on the dice")
    async def roll_dice(self, interaction: discord.Interaction, sides: int = 6):
        if sides < 1:
            await interaction.response.send_message("Dice must have at least 1 side.")
            return
        result = random.randint(1, sides)
        await interaction.response.send_message(f"You rolled: **{result}**")

    @app_commands.command(name="flip_coin", description="Flipping a coin")
    async def flip_coin(self, interaction: discord.Interaction):
        result = random.choice(["Heads", "Tails"])
        await interaction.response.send_message(f"It's: **{result}**!")    
    
    @app_commands.command(name="shuffle", description="Shuffle a list of items")
    @app_commands.describe(items="Comma-separated items to shuffle")
    async def shuffle(self, interaction: discord.Interaction, items: str):
        item_list = [item.strip() for item in items.split(',') if item.strip()]
        if len(item_list) < 2:
            await interaction.response.send_message("Provide at least two items to shuffle.")
            return
        random.shuffle(item_list)
        await interaction.response.send_message(f"Shuffled: {', '.join(item_list)}")
    
    @app_commands.command(name="yes_or_no", description="Get a simple yes or no")
    async def yes_or_no(self, interaction: discord.Interaction):
        answer = random.choice(["Yes", "No"])
        await interaction.response.send_message(answer)
    
async def setup(bot):
    await bot.add_cog(Games(bot))