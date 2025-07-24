import os
from dotenv import load_dotenv
import discord
from discord.ext import commands

load_dotenv() # .env file read
TOKEN = os.getenv('DISCORD_BOT_TOKEN')

intents = discord.Intents.all()
intents.voice_states = True

bot = commands.Bot(command_prefix=commands.when_mentioned, intents=discord.Intents.all())
    
@bot.event
async def on_ready():
    try:
        synced = await bot.tree.sync()
        print(f"🔁 Synced {len(synced)} slash command(s)")
    except Exception as e:
        print(f"Sync failed: {e}")
    print(f'{bot.user} is ON')


async def load_cogs():
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            print(f"📁 Loading cog: {filename}")
            await bot.load_extension(f'cogs.{filename[:-3]}')

async def main():
    async with bot:
        await load_cogs()
        await bot.start(TOKEN)

import asyncio
asyncio.run(main())
