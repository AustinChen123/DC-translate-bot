import discord
from discord.ext import commands
from cogs.TranslateCog import TranslateCog
import json
import asyncio


with open('credentials.json', 'r', encoding='utf-8') as f:
    CREDENTIALS = json.loads(f.read())
TOKEN = CREDENTIALS["token"]
intents = discord.Intents.default()
intents.messages  = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name}")
async def main():
    async with bot:
        await load_extensions()
        await bot.start(TOKEN)

asyncio.run(main())