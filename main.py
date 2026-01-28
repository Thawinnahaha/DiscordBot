from time import sleep

import discord
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os
import asyncio
from gtts import gTTS


from insult import generateInsult

load_dotenv()
token = os.getenv("DISCORD_TOKEN")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")






handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')#name von file, zeichenencode, modus ist write
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix=';', intents=intents) #declare den Bot bzw. die Commands

@bot.event
async def on_ready():
    print(f"W Sigma!! {bot.user.name}, has connected to Discord!")

@bot.event
async def on_member_join(member):
    await member.send(f"Welcome {member.name}, welcome message!")


@bot.event
async def on_message(message):
    if message.author == bot.user:
        await asyncio.sleep(120)
        try:
            await message.delete()
        except discord.Forbidden:
            pass

    if "shit" in message.content.lower():
        await message.channel.send(f"{message.author.mention}, nuh uh piss better")
    if "diktatur" in message.content.lower():
        await message.delete()
        await message.channel.send(f"{message.author.mention}, du Hund unser Führer Adrian ist die GOAT!!")
    if "ezfrags" in message.content.lower():
        await message.channel.send("<:66865868:1466122072789880854>")

    await bot.process_commands(message)

@bot.event
async def on_command_error(ctx, error):
    await ctx.send(f"Error: {error}")

@bot.command()
async def ping(ctx):
    await ctx.send(f"Pong! {round(bot.latency * 1000)}ms")




@bot.command()
async def insult(ctx, usr):

    await ctx.message.delete()


    user_id = usr.strip('<@!>')

    try:
        user = await bot.fetch_user(int(user_id))
        ipt = generateInsult()
        await ctx.send(f"{user.mention}, {ipt}")
    except (ValueError, discord.NotFound):
        await ctx.send("Invalid user mention.")


@bot.command()
async def join(ctx):
    await ctx.message.delete()
    if ctx.author.voice is None:
        await ctx.send("You are not in a voice channel.")
        return

    channel = ctx.author.voice.channel

    if ctx.voice_client is not None:
        await ctx.voice_client.move_to(channel)
    else:
        await channel.connect()
        await ctx.send(f"Joined {channel.mention}")

@bot.command()
async def leave(ctx):
    await ctx.message.delete()
    channel = ctx.author.voice.channel

    if ctx.voice_client is not None:
        await ctx.send(f"Leaving {channel.mention}")
        await ctx.voice_client.disconnect()
    else:
        await ctx.send("I am not in a voice channel")


@bot.command()
async def say(ctx, lang, *, msg):
    await ctx.message.delete()

    if ctx.voice_client is None:
        await ctx.send("I am not in a voice channel.")
        return # <- um den Command zu closen !!Wichtig!!

    tts = gTTS(text=msg, lang=lang)
    tts.save("voice.mp3")
    ctx.voice_client.play(discord.FFmpegPCMAudio("voice.mp3"))

    while ctx.voice_client.is_playing():
        await asyncio.sleep(1)

    os.remove("voice.mp3")






bot.run(token,log_handler=handler, log_level=logging.DEBUG)