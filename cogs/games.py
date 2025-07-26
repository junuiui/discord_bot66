import random
import discord
from discord import app_commands
from discord.ext import commands
from datetime import datetime, timedelta
import asyncio

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
        
        await interaction.response.defer(thinking=True)
        await asyncio.sleep(1) 
        
        await interaction.followup.send(f"Random number between `{start}` and `{end}`: **{number}**")
        
    @app_commands.command(name="choose", description="Choose one from the given options")
    @app_commands.describe(options="Type options separated by commas (e.g. A, B, C)")
    async def choose(self, interaction: discord.Interaction, options: str):
        items = [item.strip() for item in options.split(",") if item.strip()]
        if len(items) < 2:
            await interaction.response.send_message("Please enter at least two options, separated by commas.", ephemeral=True)
            return
        choice = random.choice(items)
        question = ', '.join(items)
        
        await interaction.response.defer(thinking=True)
        await asyncio.sleep(1) 
        await interaction.followup.send(f"From **{question}**\nResult: **{choice}**")
        
    @app_commands.command(name="roll_dice", description="Roll a dice")
    @app_commands.describe(sides="Number of sides on the dice")
    async def roll_dice(self, interaction: discord.Interaction, sides: int = 6):
        if sides < 1:
            await interaction.response.send_message("Dice must have at least 1 side.")
            return
        result = random.randint(1, sides)
        
        await interaction.response.defer(thinking=True)
        await asyncio.sleep(1) 
        await interaction.followup.send(f"You rolled: **{result}**")

    @app_commands.command(name="flip_coin", description="Flipping a coin")
    async def flip_coin(self, interaction: discord.Interaction):
        result = random.choice(["Heads", "Tails"])
        await interaction.response.defer(thinking=True)
        await asyncio.sleep(1) 
        await interaction.followup.send(f"It's: **{result}**!")    
    
    @app_commands.command(name="shuffle", description="Shuffle a list of items")
    @app_commands.describe(items="Comma-separated items to shuffle")
    async def shuffle(self, interaction: discord.Interaction, items: str):
        item_list = [item.strip() for item in items.split(',') if item.strip()]
        if len(item_list) < 2:
            await interaction.response.send_message("Provide at least two items to shuffle.")
            return
        random.shuffle(item_list)
        
        await interaction.response.defer(thinking=True)
        await asyncio.sleep(1) 
        await interaction.followup.send(f"Shuffled: {', '.join(item_list)}")
    
    @app_commands.command(name="yes_or_no", description="Get a simple yes or no")
    async def yes_or_no(self, interaction: discord.Interaction):
        answer = random.choice(["Yes", "No"])
        
        await interaction.response.defer(thinking=True)
        await asyncio.sleep(1) 
        await interaction.followup.send(answer)
    
    @app_commands.command(name="random_date", description="Get a random date between two dates")
    @app_commands.describe(start="Start date in YYYY-MM-DD", end="End date in YYYY-MM-DD")
    async def random_date(self, interaction: discord.Interaction, start: str, end: str):
        try:
            start_date = datetime.strptime(start, "%Y-%m-%d")
            end_date = datetime.strptime(end, "%Y-%m-%d")
        except ValueError:
            await interaction.response.send_message("Invalid date format. Use YYYY-MM-DD")
            return

        if start_date > end_date:
            await interaction.response.send_message("Start date must be before end date")
            return
        
        delta = end_date - start_date
        random_day = start_date + timedelta(days=random.randint(0, delta.days))
        
        await interaction.response.defer(thinking=True)
        await asyncio.sleep(1) 
        await interaction.followup.send(f"Random date: **{random_day.strftime('%Y-%m-%d')}**")
    
    @app_commands.command(name="rock_paper_scissors", description="Play Rock Paper Scissors with Azure")
    @app_commands.describe(choice="Choose rock, paper, or scissors")
    async def rock_paper_scissors(self, interaction: discord.Interaction, choice: str):
        user_choice = choice.lower()
        valid_choices = ["rock", "paper", "scissors"]
        
        if user_choice not in valid_choices:
            await interaction.response.send_message("Please choose `rock`, `paper`, or `scissors`.", ephemeral=True)
            return

        bot_choice = random.choice(valid_choices)

        result = ""
        if user_choice == bot_choice:
            result = "It's a tie! 🤝"
        elif (user_choice == "rock" and bot_choice == "scissors") or \
             (user_choice == "paper" and bot_choice == "rock") or \
             (user_choice == "scissors" and bot_choice == "paper"):
            result = "You win!"
        else:
            result = "Azure wins!"

        embed = discord.Embed(title="Rock Paper Scissors", color=discord.Color.blurple())
        embed.add_field(name="You chose", value=user_choice.capitalize(), inline=True)
        embed.add_field(name="Azure chose", value=bot_choice.capitalize(), inline=True)
        embed.add_field(name="Result", value=result, inline=False)

        await interaction.response.send_message(embed=embed)
        
    @app_commands.command(name="8ball", description="Ask the magic 8-ball a question")
    @app_commands.describe(question="Your yes/no question")
    async def eight_ball(self, interaction: discord.Interaction, question: str):
        responses = [
            "It is certain.", "Without a doubt.", "You may rely on it.",
            "Yes – definitely.", "Most likely.", "Outlook good.",
            "Yes.", "Signs point to yes.", "Reply hazy, try again.",
            "Ask again later.", "Better not tell you now.",
            "Don't count on it.", "My reply is no.",
            "Very doubtful.", "Outlook not so good."
        ]
        response = random.choice(responses)
        await interaction.response.send_message(f"Hmm... {response}")
    
    
async def setup(bot):
    await bot.add_cog(Games(bot))