import discord
from discord.ext import commands

client =  commands.Bot(command_prefix = '.')

@client.event
async def on_ready():
    print('Bot is ready.')


@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send('Invalid command')
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send('You do not have permition for that')
        await ctx.message.delete()
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Please enter the requiered args')
    else:
        raise error

@client.command()
async def clear(ctx, amount : int):
    await ctx.channel.purge(limit = amount)

@clear.error
async def clear_error(ctx, error):
    await ctx.send('Specify an amount of mesages to delete')

client.run('ODA1NTAzMDYxMjQ5NDkxMDM1.YBb1Lw.kTvnuYsO_STUKlM8Xq56GqVr2d8')