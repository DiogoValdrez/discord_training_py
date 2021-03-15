import discord
from discord.ext import commands
from discord.ext.commands.core import command

class Example2(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def test(self, ctx):
        await ctx.send('test')
    
def setup(client):
    client.add_cog(Example2(client))