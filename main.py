import discord
from discord.ext import commands
import json
import aiohttp
import asyncio
import os

with open("configuration.json", "r") as config: 
	data = json.load(config)
	token = data["token"]
	prefix = data["prefix"]
	owner_id = data["owner_id"]

intents = discord.Intents.all()
bot = commands.Bot(prefix, intents = intents, owner_id = owner_id)

@bot.event
async def on_ready():
	print(f"We have logged in as {bot.user}")
	print(discord.__version__)
	await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name =f"{bot.command_prefix}help"))

@bot.command(aliases=['gni', 'gno', 'recognise', 'song'])
async def recognize(ctx, url = None):
    if url is None:
        if ctx.message.attachments:
            attachment = ctx.message.attachments[0]
            url = attachment.url
        else:
            em = discord.Embed(title = "No attachement or URL!", description="Hey man you gotta send a file or a URL to recognize the music from -_-")
            await ctx.send(embed=em)
            return
    query_url = f"https://some-cool-api.herokuapp.com/v2/recognize_music/?url={url}"
    async with aiohttp.ClientSession() as session:
        async with session.get(query_url) as resp:
            res = await resp.json(content_type=None)
    title = res['title']
    background = res['background']
    coverart = res['url']['youtube']['thumbnail']
    url = res['url']['youtube']['video_url']
    subtitle = res['subtitle']
    em = discord.Embed(title = title, url=url, description=f"by **{subtitle}**", color = discord.Color.random())
    em.set_image(url=coverart)
    await ctx.reply(embed=em)

bot.run(token)