import discord
import json
import os
import random
from discord.ext import commands

os.chdir('/home/diogo-valdrez/my_Code/Training_Bot')

client = commands.Bot(command_prefix='.')


@client.event
async def on_ready():
    print('Ready')
    await client.change_presence(activity= discord.Game('.help'))


@client.command()
async def balance(ctx):
    await open_account(ctx.author)
    user = ctx.author
    users = await get_bank_data()
    wallet_amt = users[str(user.id)]['wallet']
    bank_amt = users[str(user.id)]['bank'] 
    em = discord.Embed(title = f"{user.name}'s balance", color = discord.Color.red())
    em.add_field(name = 'Wallet balance', value=wallet_amt)
    em.add_field(name='Bank balance', value=bank_amt)
    await ctx.send(embed = em)


@client.command()
async def beg(ctx):
    await open_account(ctx.author)
    users = await get_bank_data()
    earnings = random.randrange(101)
    await ctx.send(f"Someone gave you {earnings} coins")
    users[str(ctx.author.id)]['wallet'] += earnings
    with open('main_bank.json', 'w') as f:
        json.dump(users, f)


async def open_account(user):
    users = await get_bank_data()
    if str(user.id) in users:
        return False
    else:
        users[str(user.id)] = {}
        users[str(user.id)]['wallet'] = 0
        users[str(user.id)]['bank'] = 0
    with open('main_bank.json', 'w') as f:#talvez identação errada?
        json.dump(users, f)
    return True


async def get_bank_data():
    with open('main_bank.json', 'r') as f:
        users = json.load(f)
    return users


client.run('ODA1NTAzMDYxMjQ5NDkxMDM1.YBb1Lw.kTvnuYsO_STUKlM8Xq56GqVr2d8')

