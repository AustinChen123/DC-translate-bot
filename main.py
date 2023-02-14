import discord
from discord.ext import commands
from cogs.TranslateCog import TranslateCog
import json
import asyncio
import aiohttp


class MyBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.messages  = True
        super().__init__(command_prefix='$', intents=intents)
        self.initial_extensions = [
            'cogs.TranslateCog'
        ]

    async def setup_hook(self):
        self.background_task.start()
        self.session = aiohttp.ClientSession()
        for ext in self.initial_extensions:
            await self.load_extension(ext)

    async def close(self):
        await super().close()
        await self.session.close()

    @tasks.loop(minutes=10)
    async def background_task(self):
        print('Running background task...')

    async def on_ready(self):
        print('Ready!')

with open('credentials.json', 'r', encoding='utf-8') as f:
    CREDENTIALS = json.loads(f.read())
TOKEN = CREDENTIALS["token"]
bot = MyBot()
bot.run(TOKEN)


# @bot.event
# async def on_ready():
#     print(f"Logged in as {bot.user.name}")
# async def main():
#     async with bot:
#         await bot.load_extensions("cogs.TranslateCog")
#         await bot.start(TOKEN)

# asyncio.run(main())