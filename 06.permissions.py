import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

client =  commands.Bot(command_prefix = '.')

@client.event
async def on_ready():
    print('Bot is ready')
    
@client.command()
@commands.has_permissions(manage_messages = True)
async def clear(ctx, amount = 10):
    await ctx.channel.purge(limit=amount)

def is_it_me(ctx):
    return ctx.author.id ==  451471195049689088

@client.command()
@commands.check(is_it_me)
async def example(ctx):
    await ctx.send(f'Hi im {ctx.author}')

load_dotenv()
client.run(os.getenv('TOKEN'))