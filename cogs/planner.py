import discord
from discord import app_commands
from discord.ext import commands
import json
import os
from datetime import datetime

class Planner(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.filename = "plans.json"
        self.load_plans()

    def load_plans(self):
        if os.path.exists(self.filename):
            with open(self.filename, "r", encoding="utf-8") as f:
                self.plans = json.load(f)
        else:
            self.plans = []

    def save_plans(self):
        with open(self.filename, "w", encoding="utf-8") as f:
            json.dump(self.plans, f, ensure_ascii=False, indent=2)

    def time_left_str(self, target_dt):
        now = datetime.now()
        delta = target_dt - now
        if delta.total_seconds() < 0:
            return "Time passed"
        days = delta.days
        hours = delta.seconds // 3600
        return f"{days} days, {hours} hours left"

    @app_commands.command(name="plan_add", description="Add a new plan with date and time")
    @app_commands.describe(
        date="Date of plan (YYYY-MM-DD)",
        time="Time of plan (HH:MM, 24-hour format)",
        content="Plan content",
        people="People involved (comma separated)",
        place="Place"
    )
    async def plan_add(self, interaction: discord.Interaction, date: str, time: str, content: str, people: str, place: str):
        # Validate date and time
        try:
            dt_str = f"{date} {time}"
            plan_dt = datetime.strptime(dt_str, "%Y-%m-%d %H:%M")
        except ValueError:
            await interaction.response.send_message("Invalid date or time format.\nDate: YYYY-MM-DD\nTime: HH:MM (24h)", ephemeral=True)
            return

        plan_id = len(self.plans) + 1
        new_plan = {
            "id": plan_id,
            "datetime": dt_str,
            "content": content,
            "people": [p.strip() for p in people.split(",") if p.strip()],
            "place": place
        }
        self.plans.append(new_plan)
        self.save_plans()

        await interaction.response.send_message(f"Plan added with ID {plan_id}!")

    @app_commands.command(name="plan_list", description="List all plans with time left")
    async def plan_list(self, interaction: discord.Interaction):
        if not self.plans:
            await interaction.response.send_message("No plans saved yet.", ephemeral=True)
            return

        msg = "**Saved Plans:**\n"
        for p in self.plans:
            plan_dt = datetime.strptime(p["datetime"], "%Y-%m-%d %H:%M")
            time_left = self.time_left_str(plan_dt)
            msg += (f"ID: {p['id']} | DateTime: {p['datetime']} | Time left: {time_left}\n"
                    f"Content: {p['content']} | People: {', '.join(p['people'])} | Place: {p['place']}\n\n")

        await interaction.response.send_message(msg, ephemeral=True)

    @app_commands.command(name="plan_delete", description="Delete a plan by ID")
    @app_commands.describe(plan_id="ID of plan to delete")
    async def plan_delete(self, interaction: discord.Interaction, plan_id: int):
        original_len = len(self.plans)
        self.plans = [p for p in self.plans if p["id"] != plan_id]

        if len(self.plans) == original_len:
            await interaction.response.send_message("No plan found with that ID.", ephemeral=True)
        else:
            # Reassign IDs for consistency
            for i, p in enumerate(self.plans, start=1):
                p["id"] = i
            self.save_plans()
            await interaction.response.send_message(f"Plan ID {plan_id} deleted.")

    @app_commands.command(name="plan_latest", description="Show the most recent plan with time left")
    async def plan_latest(self, interaction: discord.Interaction):
        if not self.plans:
            await interaction.response.send_message("No plans saved yet.", ephemeral=True)
            return

        sorted_plans = sorted(self.plans, key=lambda x: datetime.strptime(x["datetime"], "%Y-%m-%d %H:%M"))
        latest = sorted_plans[0]
        plan_dt = datetime.strptime(latest["datetime"], "%Y-%m-%d %H:%M")
        time_left = self.time_left_str(plan_dt)

        msg = (f"**Latest Plan:**\n"
               f"ID: {latest['id']} | DateTime: {latest['datetime']} | Time left: {time_left}\n"
               f"Content: {latest['content']} | People: {', '.join(latest['people'])} | Place: {latest['place']}")
        await interaction.response.send_message(msg)

async def setup(bot):
    await bot.add_cog(Planner(bot))
