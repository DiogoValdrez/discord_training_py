import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

client = commands.Bot(command_prefix='.', intents = discord.Intents.all())#tambem se pode usar default

load_dotenv()
client.run(os.getenv('TOKEN'))

