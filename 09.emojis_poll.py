import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

client = commands.Bot(command_prefix='.')

@client.event
async def on_ready():
    print('Ready')
#the emoji id is in the image location
#pode se usar emojipedia

@client.event
async def on_message(msg):
    if ':' == msg.content[0] and ':' == msg.content[-1]:
        emoji_name = msg.content[1:-1]
        for emoji in msg.guild.emojis:
            if emoji_name == emoji.name:
                await msg.channel.send(str(emoji))
                await msg.delete()
                break
    if 'cool' in msg.content:
        await msg.add_reaction('🔥')
    await client.process_commands(msg)#IMPORTANTEEEE
        
@client.command()
async def emoji(ctx):
    await ctx.send('🔥')
    await ctx.send(':fork_and_knife:')#so deve funcionar com emojis officiais normalmente poe-se <:nomeemoji:codigo>  # se for animado é so <a:nome:codigo>
    await ctx.send('1')

@client.command(aliases=['p'])
async def poll(ctx, *, msg):
    channel = ctx.channel
    try:
        op1, op2 = msg.split('or')
        txt = f'React with 1️⃣ for {op1} or 2️⃣ for {op2}'
    except:
        await channel.send('Correct Syntax: [Choice 1] or [Choice 2]')
        return
    embed = discord.Embed(title = 'Poll', description = txt, color = discord.Colour.red())
    message_ = await channel.send(embed=embed)
    await message_.add_reaction('1️⃣')
    await message_.add_reaction('2️⃣')
    await ctx.message.delete()


load_dotenv()
client.run(os.getenv('TOKEN'))

