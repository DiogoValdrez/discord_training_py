import discord
from discord.ext import commands
import random

client =  commands.Bot(command_prefix = '.')

filtered_words = ['test', 'test2']

@client.event
async def on_ready():
    print('Bot is ready.')

@client.event
async def on_message(msg):
    for word in filtered_words:
        if word in msg.content:
            await msg.delete()
    await client.process_commands(msg)

@client.event
async def on_member_join(member):
    print(f'{member} has joined a server.')

@client.event
async def on_member_removed(member):
    print(f'{member} has left a server.')

@client.command()
async def ping(ctx):
    await ctx.send(f'Pong!\n{round(client.latency* 1000)} ms')#await significa que n executa mais nada ate acabar de executar esta linha

@client.command(aliases=['8ball', 'test'])
async def _8ball(ctx, *, question):
    # o * significa que todo o imput após * pertence a question
    responses = ['It is certain.',
    'It is decidedly so.',
    'Without a doubt.',
    'Yes – definitely.',
    'You may rely on it.',
    'As I see it, yes.',
    'Most likely.',
    'Outlook good.',
    'Yes.',
    'Signs point to yes.',
    'Reply hazy, try again.',
    'Ask again later.',
    'Better not tell you now.',
    'Cannot predict now.',
    'Concentrate and ask again.',
    "Don't count on it.",
    'My reply is no.',
    'My sources say no.',
    'Outlook not so good.',
    'Very doubtful.']
    await ctx.send(f'Question: {question}\nAnswer: {random.choice(responses)}')

@client.command()
@commands.has_permissions(manage_messages = True)
async def clear(ctx, amount = 5):
    await ctx.channel.purge(limit = amount + 1)

@client.command()
async def kick(ctx, member : discord.member, *,reason = 'none'):
    await member.kick(reason = reason)
    await ctx.send(f'Banned {member.mention}')
    await member.send(reason = reason)

@client.command()#pode n funcionar caso as dms estejam fechadas
async def ban(ctx, member : discord.member, *,reason = 'none'):
    await member.ban(reason = reason)
    await ctx.send(f'Banned {member.mention}')
    await member.send(reason = reason)

@client.command()
async def unban(ctx, *, member):
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = member.split('#')

    for ban_entry in banned_users:
        user = ban_entry.user

        if (user.name, user.discriminator) == (member_name, member_discriminator):
            await ctx.guild.unban(user)
            await ctx.send(f'Unbanned {user.mention}')
            return

@client.command
@commands.has_permissions(kick_members = True)#tem de exisitr o role mute
async def mute(ctx, member : discord.Member):
    muted_role = ctx.guild.get_role()#id do mute role
    await member.add_roles(muted_role)
    await ctx.send(member.mention + "has been muted")


client.run('ODA1NTAzMDYxMjQ5NDkxMDM1.YBb1Lw.kTvnuYsO_STUKlM8Xq56GqVr2d8')