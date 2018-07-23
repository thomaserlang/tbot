print('INIT!!!')
try:
    import discord
except ImportError:
    raise Exception('''
        The discord libary must be installed manually:
            pip install https://github.com/Rapptz/discord.py/archive/rewrite.zip
    ''')

from discord.ext import commands

bot = commands.Bot(command_prefix='!')