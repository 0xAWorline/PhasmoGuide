import discord
import json
from discord import message
from discord import file
from discord.embeds import Embed
from discord.ext import commands
from discord.ext.commands import context
from discord.ext.commands.core import command
#from discord.member import Member

class GameWiki(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def hello(self, ctx):
        await ctx.send("Hello There!")


def setup(bot):
    bot.add_cog(GameWiki(bot))