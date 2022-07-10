import discord
from discord.ext import commands

class tcog(commands.Cog):
    @commands.command(name="test1")
    @commands.has_permissions(administrator=True)
    async def test(self, ctx):
        await ctx.send('test')
        pass
