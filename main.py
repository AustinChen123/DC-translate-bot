import discord
from discord.ext import commands
from cogs.TranslateCog import TranslateCog
import json


with open('credentials.json', 'r', encoding='utf-8') as f:
    CREDENTIALS = json.loads(f.read())
TOKEN = CREDENTIALS["token"]
bot = commands.Bot(command_prefix="!")

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name}")

bot.add_cog(TranslateCog(bot))


bot.run(TOKEN)
