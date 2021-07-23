import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

client =  commands.Bot(command_prefix = '.')

@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.idle, activity=discord.Game('Hello there!'))
    print('Bot is ready.')

load_dotenv()
client.run(os.getenv('TOKEN'))