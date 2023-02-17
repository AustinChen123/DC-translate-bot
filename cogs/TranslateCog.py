import discord
from discord.ext import commands
from discord import Client
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

        Name = message.author.display_name
        Avatar = message.author.display_avatar.url
        guild_id = message.channel.guild.id
        message_channel = message.channel.id
        text = message.content
        attachments = message.attachments
            
        if self.config.get(str(guild_id)):
            if self.config[str(guild_id)].get("read_channel_id"):
                read_channel_id = self.config[str(guild_id)]["read_channel_id"]
            if self.config[str(guild_id)].get("reply_channel_id"):
                reply_channel_id = self.config[str(guild_id)]["reply_channel_id"]
        if message.author == self.bot.user:
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
                await target_channel.send("Sorry, you have exceed the deepl daily translate limit.")
                return
            translated_text = result['translations'][0]['text']

 
 
        webhook = await target_channel.create_webhook(name=Name)
        if text != "":
            await webhook.send(
                str(translated_text), username=Name, avatar_url=Avatar)

        if len(attachments) !=0:
            for attachment in attachments:
                await webhook.send(
                    attachment.url, username=Name, avatar_url=Avatar)
    
        webhooks = await target_channel.webhooks()
        for webhook in webhooks:
            await webhook.delete()


    # @commands.command()
    # async def set_read_channel(self, ctx, read_channel: discord.TextChannel):
    #     if ctx.channel.permissions_for(ctx.author).administrator:
    #         if config.get(str(channel.guild.id)):
    #             config[str(channel.guild.id)]["read_channel_id"] = read_channel.id
    #         else:
    #             config[str(channel.guild.id)] = {}
    #             config[str(channel.guild.id)]["read_channel_id"] = read_channel.id
    #         with open(os.path.abspath('config.json'), "w") as outfile:
    #             json.dump(config, outfile) 
    #         await ctx.send(f"Start reading channel <#{read_channel.id}>")
    #     else:
    #         await ctx.send("Sorry, you have no permission to use this command")
        
    @commands.command()
    async def set_reply_channel(self, ctx, reply_channel: discord.TextChannel):
        if ctx.channel.permissions_for(ctx.author).administrator:
            if config.get(str(channel.guild.id)):
                config[str(channel.guild.id)]["reply_channel_id"] = reply_channel.id
            else:
                config[str(channel.guild.id)] = {}
                config[str(channel.guild.id)]["reply_channel_id"] = reply_channel.id
            with open(os.path.abspath('config.json'), "w") as outfile:
                json.dump(config, outfile) 
            await ctx.send(f"Replying to channel <#{reply_channel.id}>")
        else:
            await ctx.send("Sorry, you have no permission to use this command")

async def setup(bot):
    await bot.add_cog(TranslateCog(bot))