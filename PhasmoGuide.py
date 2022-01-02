import os
from typing import AnyStr
from dotenv import load_dotenv
import discord
from discord import message
from discord.ext import commands
from re import search

intents = discord.Intents().all()
bot = commands.Bot(command_prefix='$', intents=intents)

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")

@bot.command()
async def load(ctx, extension):
	bot.load_extension(f'cogs.{extension}')
	await ctx.send(f'{extension} has been loaded.')
	print(f'cogs.{extension} has been loaded.')

@bot.command()
async def reload(ctx, extension):
	bot.reload_extension(f'cogs.{extension}')
	await ctx.send(f'{extension} has been reloaded.')
	print(f'cogs.{extension} has been reloaded.')

@bot.command()
async def unload(ctx, extension):
	bot.unload_extension(f'cogs.{extension}')
	await ctx.send(f'{extension} has been unloaded.')
	print(f'cogs.{extension} has been unloaded.')

for filename in os.listdir('./cogs'):
	if filename.endswith('.py'):
		bot.load_extension(f'cogs.{filename[:-3]}')

@bot.command()
async def ping(ctx):
	await ctx.send(f"Pong! {round(bot.latency * 1000)}ms")
@bot.event
async def on_command_error(ctx, error):
	if isinstance(error, commands.CommandNotFound):
		await ctx.send('Command does not exist.')

@bot.command()
async def echo(ctx, message: str):
	await ctx.send(message)

@bot.event
async def on_ready():
	await bot.change_presence(status=discord.Status.online, activity=discord.Game('Lets get our spook on!'))
	print(f'{bot.user} has connected to Discord!')

@bot.event
async def on_message(message):
	if message.author == bot.user:
		return
	await bot.process_commands(message)

bot.run(TOKEN)