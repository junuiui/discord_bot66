# disabled. 

from discord.ext import commands
from discord import app_commands, Interaction
import openai
import os

class AI(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.api_key = os.getenv("OPENAI_API_KEY")
        openai.api_key = self.api_key

    @app_commands.command(name="ask", description="Ask GPT something!")
    @app_commands.describe(question="What do you want to ask GPT?")
    async def ask(self, interaction: Interaction, question: str):
        
        # disabled
        await interaction.response.send_message("Sorry! The /ask command is temporarily unavailable due to a technical issue.", ephemeral=True)
        return
        #####################
        
        if not self.api_key:
            await interaction.response.send_message("/ask is currently disabled.", ephemeral=True)
            return
        await interaction.response.defer(thinking=True)
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": question}
                ]
            )
            answer = response.choices[0].message.content.strip()
            await interaction.followup.send(f"**Q:** {question}\n**A:** {answer}")
        except Exception as e:
            await interaction.followup.send(f"Error: {e}")

async def setup(bot):
    await bot.add_cog(AI(bot))
