import discord
import random
from discord.ext import commands, tasks

client = commands.Bot(command_prefix='.')
images = ['https://i.imgur.com/gAWGNnn.jpg',
'https://i.imgur.com/iFkeKAw.jpg']

@client.event
async def on_ready():
    print('Game on!')

@client.command(aliases=['user', 'info'])
@commands.has_permissions(kick_members = True)
async def whois(ctx,member : discord.Member):
    embed = discord.Embed(title = member.name, description = member.mention, color = discord.Colour.green())
    embed.add_field(name = 'ID', value = member.id, inline = True)#inline significa se esta ou na mesma linha
    embed.set_thumbnail(url = member.avatar_url)
    embed.set_footer(icon_url = ctx.author.avatar_url, text = f"Resquested by {ctx.author.name}")
    await ctx.send(embed=embed)

@client.command()
async def image(ctx):
    embed = discord.Embed(color = discord.Colour.red())
    random_link = random.choice(images)
    embed.set_image(url = random_link)
    await ctx.send(embed = embed)
    #await ctx.author.send(embed = embed) #assim enviaria para as DM

client.run('ODA1NTAzMDYxMjQ5NDkxMDM1.YBb1Lw.kTvnuYsO_STUKlM8Xq56GqVr2d8')

