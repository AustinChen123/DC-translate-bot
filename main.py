import discord
from discord.ext import commands, tasks
from cogs.TranslateCog import TranslateCog
from discord import app_commands    
import json
import os

class MyBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        # intents.messages  = True
        intents.message_content = True
        super().__init__(command_prefix="/",intents=intents)
        self.initial_extensions = [
            'cogs.TranslateCog'
        ]

    async def setup_hook(self):
        for ext in self.initial_extensions:
            await self.load_extension(ext)

    async def close(self):
        await super().close()

    async def on_ready(self):
        await self.tree.sync()
        print('Ready!')

with open('credentials.json', 'r', encoding='utf-8') as f:
    CREDENTIALS = json.loads(f.read())
TOKEN = CREDENTIALS["token"]


bot = MyBot()

@bot.tree.command(name="set_read_channel", description="make the bot listen to a specific channel")
# @tree.command(name="set_read_channel", description="make the bot listen to a specific channel")
async def self(interaction:discord.Interaction, channel: discord.TextChannel):
    
    if channel.permissions_for(interaction.user).administrator:
        config = {}
        with open(os.path.abspath('config.json'), 'r') as f:
            config = json.loads(f.read())
        if config.get(str(channel.guild.id)):
            config[str(channel.guild.id)]["read_channel_id"] = channel.id
        else:
            config[str(channel.guild.id)] = {}
            config[str(channel.guild.id)]["read_channel_id"] = channel.id
        with open(os.path.abspath('config.json'), "w") as outfile:
            json.dump(config, outfile) 
        await interaction.response.send_message(f"Start reading channel <#{channel.id}>")
    else:
        await interaction.response.send_message("Sorry, you have no permission to use this command")
@bot.tree.command(name="set_reply_channel", description="make the bot reply to a specific channel")
# @tree.command(name="set_read_channel", description="make the bot listen to a specific channel")
async def self(interaction:discord.Interaction, channel: discord.TextChannel):
    if channel.permissions_for(interaction.user).administrator:
        config = {}
        with open(os.path.abspath('config.json'), 'r') as f:
            config = json.loads(f.read())
        if config.get(str(channel.guild.id)):
            config[str(channel.guild.id)]["reply_channel_id"] = channel.id
        else:
            config[str(channel.guild.id)] = {}
            config[str(channel.guild.id)]["reply_channel_id"] = channel.id
        with open(os.path.abspath('config.json'), "w") as outfile:
            json.dump(config, outfile) 
        await interaction.response.send_message(f"Start reply to channel <#{channel.id}>")
    else:
        await interaction.response.send_message("Sorry, you have no permission to use this command")
bot.run(TOKEN)


# @bot.event
# async def on_ready():
#     print(f"Logged in as {bot.user.name}")
# async def main():
#     async with bot:
#         await bot.load_extensions("cogs.TranslateCog")
#         await bot.start(TOKEN)

# asyncio.run(main())