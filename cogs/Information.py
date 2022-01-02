import discord
import json
from discord import message
from discord import file
from discord.embeds import Embed
from discord.ext import commands
from discord.ext.commands import context
from discord.ext.commands.core import command
#from discord.member import Member

class GhostLookUp(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

def setup(bot):
    bot.add_cog(GhostLookUp(bot))