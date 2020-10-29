import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.presences = True
intents.members = True

bot = commands.Bot(command_prefix='>', help=None, intents=intents)