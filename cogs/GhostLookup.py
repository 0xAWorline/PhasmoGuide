from os import name
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

    @commands.command(aliases=["getinfo"], help="Supply the type of ghost to learn more about it")
    async def getInfo(self, ctx, message: str):
        with open("storage.json", "r") as file:
            data = json.load(file)
        file.close()

        ghosts = data["GhostTypes"]
        for ghost in ghosts:
            if(ghost["Name"] == message):
                embed = discord.Embed(title=ghost["Name"],
                description=ghost["Description"],
                color=discord.Color.blue())
                embed.add_field(name="Strengths:", value=ghost["Strengths"], inline=False)
                embed.add_field(name="Weaknesses:", value=ghost["Weaknesses"], inline=False)
                embed.add_field(name="Evidence #1", value=ghost["EvidenceTypes"][0], inline=True)
                embed.add_field(name="Evidence #2", value=ghost["EvidenceTypes"][1], inline=True)
                embed.add_field(name="Evidence #3", value=ghost["EvidenceTypes"][2], inline=True)
                embed.set_footer(icon_url=ctx.author.avatar_url, text=f"Information requested by: {ctx.message.author}")
                await ctx.send(embed=embed)

    @commands.command(help="Shows information about all the ghost types")
    async def ghosts(self, ctx):
        file = open("storage.json", "r")
        data = json.load(file)
        file.close()
        ghosts = data["GhostTypes"]
        
        pages = []
        for ghost in ghosts:
            page = discord.Embed(
                title = ghost["Name"],
                description=ghost["Description"],
                color = discord.Color.random()
            )
            page.add_field(name="Strengths:", value=ghost["Strengths"], inline=False)
            page.add_field(name="Weaknesses:", value=ghost["Weaknesses"], inline=False)
            page.add_field(name="Evidence #1", value=f"`{ghost['EvidenceTypes'][0]}`", inline=True)
            page.add_field(name="Evidence #2", value=f"`{ghost['EvidenceTypes'][1]}`", inline=True)
            page.add_field(name="Evidence #3", value=f"`{ghost['EvidenceTypes'][2]}`", inline=True)
            page.set_footer(icon_url=ctx.author.avatar_url, text=f"Information requested by {ctx.message.author}")
            pages.append(page)
            
        message = await ctx.send(embed = pages[0])
        await message.add_reaction('⏮')
        await message.add_reaction('◀')
        await message.add_reaction('▶')
        await message.add_reaction('⏭')
        
        #checks reactions to make sure only author clicks on them
        def checkAuthor(reaction, user):
            return user == ctx.author

        i = 0
        reaction = None
        while True:
            if str(reaction) == '⏮':
                i = 0
                await message.edit(embed = pages[i])
            elif str(reaction) == '◀':
                if i > 0:
                    i -= 1
                    await message.edit(embed = pages[i])
            elif str(reaction) == '▶':
                if i < (len(pages) - 1):
                    i += 1
                    await message.edit(embed = pages[i])
            elif str(reaction) == '⏭':
                i = len(pages) - 1
                await message.edit(embed = pages[i])
            
            try:
                reaction, user = await self.bot.wait_for('reaction_add', timeout = 60.0, check = checkAuthor)
                await message.remove_reaction(reaction, user)
            except:
                break
        # Clears the reactions instantly, comment out if needed for any reason.
        await message.clear_reactions()
    
    @commands.command(aliases=["guess"])
    async def Guess(self, ctx, * ,message: str):
        possibleGhostList = []
        userEvidences = []
        evidenceShortHand = {
            "ft" : "Freezing Temperatures",
            "go" : "Ghost Orb",
            "sb" : "Spirit Box",
            "gw" : "Ghost Writing",
            "e" : "EMF Level 5",
            "dp" : "DOTS Projector",
            "fp" : "Fingerprints"
        }
        print(message)
        if message == "help":
            embed = discord.Embed(title="-----Arguments Guide-----",
            description = "Use these arguments as shorthand for each evidence type",
            color = discord.Color.teal())
            embed.add_field(name="fp", value="Fingerprints", inline=True)
            embed.add_field(name="dt", value="DOTS Projector", inline=True)
            embed.add_field(name="e", value="EMF Level 5", inline=True)
            embed.add_field(name="gw", value="Ghost Writing", inline=True)
            embed.add_field(name="sb", value="Spirit Box", inline=True)
            embed.add_field(name="go", value="Ghost Orb", inline=True)
            embed.add_field(name="ft", value="Freezing Temperatures", inline=True)
            await ctx.send(embed=embed)
        
        userShortHand = message.split()
        for evidenceType in userShortHand:
            userEvidences.append(evidenceShortHand[evidenceType])
        print(userEvidences)
        
        file = open("storage.json", "r")
        data = json.load(file)
        file.close()
        ghosts = data["GhostTypes"]
        for ghost in ghosts:
            evidenceTypes = ghost["EvidenceTypes"]
            if all(evidence in evidenceTypes for evidence in userEvidences):
                possibleGhostList.append(ghost)

        if(len(possibleGhostList) > 0):  
            embed = discord.Embed(title="-----Possible Ghosts-----",
            description="These are the remaining evidences needed for each ghost type.",
            color = discord.Color.blurple())

            for possibleGhost in possibleGhostList:
                #makes list for elements that don't intersect with both lists
                excludedList = list(set(possibleGhost["EvidenceTypes"]) - set(userEvidences))
                name = possibleGhost["Name"]
                embed.add_field(name="\u200b", value=f"**__{name}__**", inline=False)
                for evidence in excludedList:
                    embed.add_field(name="Needed", value=f"`{evidence}`", inline=True)

            embed.set_footer(icon_url=ctx.author.avatar_url, text=f"Information requested by: {ctx.message.author}")
            await ctx.send(embed=embed)
        else:
            await ctx.send("Check spelling and spacing for evidences.")
            
        
def setup(bot):
    bot.add_cog(GhostLookUp(bot))