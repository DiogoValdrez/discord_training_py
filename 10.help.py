import discord
from discord.ext import commands

client = commands.Bot(command_prefix='.')
client.remove_command('help')

@client.group(invoke_without_command = True)
async def help(ctx):
    em = discord.Embed(title ='Help', description = 'Use .help <command> for extended info')
    em.add_field(name = 'Moderator', value = 'kick, ban, warn')
    em.add_field(name = 'Fun', value = '8ball,reverse')

    await ctx.send(embed = em)

@help.command()
async def kick(ctx):
    em = discord.Embed(title = 'Ping', description = 'Kikcs a member', color = discord.Colour.red())
    em.add_field(name = '**Syntax**', value = '.kick <member> [reason]')
    await ctx.send(embed = em)

client.run('ODA1NTAzMDYxMjQ5NDkxMDM1.YBb1Lw.kTvnuYsO_STUKlM8Xq56GqVr2d8')

