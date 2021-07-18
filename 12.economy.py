from operator import index
import discord
import json
import os
import random
from discord import embeds
from discord.ext import commands
from discord.ext.commands.core import wrap_callback

client = commands.Bot(command_prefix='.')


mainshop = [{"name":"Watch", "price":100, "description":"Time"},
            {"name":"Laptop", "price":1000, "description":"Work"},
            {"name":"PC", "price":10000, "description":"Gaming"},]


@client.event
async def on_ready():
    print('Ready')
    await client.change_presence(activity= discord.Game('.help'))


@client.command()
async def balance(ctx):
    """Gives back your balance in your bank and wallet"""
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


@client.command()
async def withdraw(ctx, amount = None):
    await open_account(ctx.author)  
    if amount == None:
        await ctx.send("Please enter the amount")
        return
    amount = int(amount)
    bal = await update_bank(ctx.author)
    if amount > bal[1]:
        await ctx.send("You don't have that much money in the bank!")
        return
    if amount < 0:
        await ctx.send("The withdraw amount must be positive!")
        return
    await update_bank(ctx.author, amount)
    await update_bank(ctx.author, -1*amount, "bank")
    await ctx.send(f"You withdrew {amount} coins!")


@client.command()
async def deposit(ctx, amount = None):
    await open_account(ctx.author)
    if amount == None:
        await ctx.send("Please enter the amount")
        return
    amount = int(amount)
    bal = await update_bank(ctx.author)
    if amount > bal[0]:
        await ctx.send("You don't have that much money in the wallet!")
        return
    if amount < 0:
        await ctx.send("The deposit amount must be positive!")
        return
    await update_bank(ctx.author, amount, "bank")
    await update_bank(ctx.author, -1*amount)
    await ctx.send(f"You deposited {amount} coins!")


@client.command()
async def send(ctx,member:discord.Member, amount = None):
    await open_account(ctx.author)
    await open_account(member)
    if amount == None:
        await ctx.send("Please enter the amount")
        return
    bal = await update_bank(ctx.author)
    if amount == "all":
        amount = bal[1]   
    amount = int(amount)
    if amount > bal[1]:
        await ctx.send("You don't have that much money in the bank!")
        return
    if amount < 0:
        await ctx.send("The send amount must be positive!")
        return
    await update_bank(member, amount, "bank")
    await update_bank(ctx.author, -1*amount, "bank")
    await ctx.send(f"You gave {amount} coins to {member}!")


@client.command()
async def rob(ctx,member:discord.Member):
    await open_account(ctx.author)
    await open_account(member)
    bal = await update_bank(member)
    if bal[0] < 100:
        await ctx.send("It's not worth it!")
        return
    amount = random.randrange(0, bal[0])
    await update_bank(member, -1*amount)
    await update_bank(ctx.author, amount)
    await ctx.send(f"You robbed {amount} coins from {member}!")


@client.command()
async def slots(ctx, amount = None):
    await open_account(ctx.author)
    if amount == None:
        await ctx.send("Please enter the amount")
        return
    amount = int(amount)
    bal = await update_bank(ctx.author)
    if amount > bal[0]:
        await ctx.send("You don't have that much money in the wallet!")
        return
    if amount < 0:
        await ctx.send("The bet amount must be positive!")
        return
    final = []
    for i in range(3):
        a = random.choice(["😂", "😍", "🥳", "🤯"])#it can be custoum emojis
        final.append(a)
    await ctx.send(f"{final[0]}{final[1]}{final[2]}")
    if final[0] == final[1] and final[1] == final[2]:
        amount *= 5
        await ctx.send(f"JACKPOT!🎉")
        await ctx.send(f"You won {amount} coins!")
    elif final[0] == final[1] or final[1] == final[2] or final[0] == final[2]:
        amount = int(0.5*amount)
        await ctx.send(f"You won {amount} coins!")
    else:
        amount *= -1
        await ctx.send("You lost")
    await update_bank(ctx.author, amount, "wallet")


@client.command()
async def shop(ctx):
    em = discord.Embed(title = "Shop")
    for item in mainshop:
        name = item["name"]
        price = item["price"]
        desc = item["description"]
        em.add_field(name=name, value=f"${price} | {desc}")
    await ctx.send(embed = em)


@client.command()
async def buy(ctx, item, amount = 1):
    await open_account(ctx.author)
    res =  await buy_this(ctx.author, item, amount)
    if not res[0]:
        if res[1]==1:
            await ctx.send("That Object isn't in the shop!")
            return
        if res[1]==2:
            await ctx.send(f"You dont have enough money to buy {amount} {item}")
            return
    await ctx.send(f"You just bought {amount} {item}")


@client.command()
async def bag(ctx):
    await open_account(ctx.author)
    user = ctx.author
    users = await get_bank_data()
    try:
        bag = users[str(user.id)]["bag"]
    except:
        bag = []
    em = discord.Embed(title = "Bag")
    for item in bag:
        name = item["item"]
        amount = item["amount"]
        em.add_field(name = name, value = amount)
    await ctx.send(embed = em)

async def open_account(user):
    users = await get_bank_data()
    if str(user.id) in users:
        return False
    else:
        users[str(user.id)] = {}
        users[str(user.id)]['wallet'] = 0
        users[str(user.id)]['bank'] = 0
    with open('main_bank.json', 'w') as f:
        json.dump(users, f)
    return True


async def get_bank_data():
    with open('main_bank.json', 'r') as f:
        users = json.load(f)
    return users


async def update_bank(user, change = 0, mode = "wallet"):
    users = await get_bank_data()
    users[str(user.id)][mode] += change
    with open("main_bank.json", "w") as f:
        json.dump(users,f)
    bal = [users[str(user.id)]["wallet"], users[str(user.id)]["bank"]]
    return bal


async def buy_this(user, item_name, amount):
    item_name = item_name.lower()
    name_ = None
    for item in mainshop:
        name = item["name"].lower()
        if name == item_name:
            name_ = name
            price = item["price"]
            break
    if name_ == None:
        return[False,1]
    cost = price*amount
    users = await get_bank_data()
    bal = await update_bank(user)
    if bal[0]<cost:
        return [False,2]
    try:
        index = 0
        t = None
        for thing in users[str(user.id)]["bag"]:
            n = thing["item"]
            if n == item_name:
                old_amt = thing["amount"]
                new_amt = old_amt + amount
                users[str(user.id)]["bag"][index]["amount"] = new_amt
                t = 1
                break
            index += 1
        if t == None:
            obj = {"item" : item_name, "amount" : amount}
            users[str(user.id)]["bag"].append(obj)
    except:
        obj = {"item" : item_name, "amount" : amount}
        users[str(user.id)]["bag"] = [obj]    
    with open("main_bank.json", "w") as f:
        json.dump(users,f)
    await update_bank(user, cost*-1,"wallet")
    return [True, "Worked"]


client.run('ODA1NTAzMDYxMjQ5NDkxMDM1.YBb1Lw.Tfv-I7WqLrstcEo7fPRCnKm4HgQ')#tirar a key

