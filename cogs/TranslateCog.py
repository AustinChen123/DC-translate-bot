import discord
from discord.ext import commands
import requests
import json
import googletrans



import os

with open(os.path.abspath('credentials.json'), 'r', encoding='utf-8') as f:
    CREDENTIALS = json.loads(f.read())
DEEPL_API_KEY = CREDENTIALS["DeepLApi"]
last_speaker = ""
PARAMS = {
    "last_speaker":last_speaker
}
class TranslateCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        with open(os.path.abspath('config.json'), 'r') as f:
            self.config = json.loads(f.read())
     
    @commands.Cog.listener()
    async def on_message(self, message):
        global PARAMS
        guild_id = message.channel.guild.id
        message_channel = message.channel.id
        text = message.content
        author = message.author.name
        user = await self.bot.fetch_user(message.author.id)
        avatar = user.avatar_url_as(size=32)
        if message.author == self.bot.user:
            return
        if self.config.get(str(guild_id)):
            if self.config[str(guild_id)].get("read_channel_id"):
                read_channel_id = self.config[str(guild_id)]["read_channel_id"]
            if self.config[str(guild_id)].get("reply_channel_id"):
                reply_channel_id = self.config[str(guild_id)]["reply_channel_id"]
            else:
                return
            if message_channel != read_channel_id:
                return
            else:
                target_channel = self.bot.get_channel(reply_channel_id)
                headers = {
                    'Authorization': f'DeepL-Auth-Key {DEEPL_API_KEY}',
                    'Content-Type': 'application/x-www-form-urlencoded'
                }
                data = {
                    'text': text,
                    'target_lang': 'en'
                }
                response = requests.post('https://api-free.deepl.com/v2/translate', headers=headers, data=data)

                
                result = json.loads(response.text)
                if response.status_code  == 4002:
                    await ctx.send("Sorry, you have exceed the deepl daily translate limit.")
                    return
                translated_text = result['translations'][0]['text']
                try:
                    if author != PARAMS["last_speaker"]:
                        # file = await author.display_avatar.to_file()
                        # await message.channel.send(file = file)
                        await target_channel.send(avatar)
                        await target_channel.send(f"{author} said:")
                except:
                    pass
                await target_channel.send("︱" + translated_text.replace("\n","\n︱"))
            PARAMS["last_speaker"] = message.author.name

        else:
            await ctx.send("You have not set the read/reply channel, please use`!set_channel`command first.")
            return 

    @commands.command()
    async def set_read_channel(self, ctx, read_channel: discord.TextChannel):
        if ctx.author.permissions_in(ctx.channel).administrator:
            if self.config.get(str(ctx.guild.id)):
                self.config[str(ctx.guild.id)]["read_channel_id"] = read_channel.id
            else:
                self.config[str(ctx.guild.id)] = {}
                self.config[str(ctx.guild.id)]["read_channel_id"] = read_channel.id
            with open(os.path.abspath('config.json'), "w") as outfile:
                json.dump(self.config, outfile) 
            await ctx.send(f"Start reading channel <#{read_channel.id}>")
        else:
            await ctx.send("Sorry, you have no permission to use this command")
        
    @commands.command()
    async def set_reply_channel(self, ctx, reply_channel: discord.TextChannel):
        if ctx.author.permissions_in(ctx.channel).administrator:
            if self.config.get(str(ctx.guild.id)):
                self.config[str(ctx.guild.id)]["reply_channel_id"] = reply_channel.id
            else:
                self.config[str(ctx.guild.id)] = {}
                self.config[str(ctx.guild.id)]["reply_channel_id"] = reply_channel.id
            with open(os.path.abspath('config.json'), "w") as outfile:
                json.dump(self.config, outfile) 
            await ctx.send(f"Replying to channel <#{reply_channel.id}>")
        else:
            await ctx.send("Sorry, you have no permission to use this command")

async def setup(bot):
    await bot.add_cog(MyCog(bot))