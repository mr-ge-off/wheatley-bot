#! /usr/bin/python3

from importlib import import_module
from os import environ
from discord import AllowedMentions
from discord.ext import commands
from cogs.admin import Admin
from cogs.voice import Voice
from cogs.text import Text

bot = commands.Bot(
    command_prefix=['!', '$'],
    allowed_mentions=AllowedMentions()
)

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')


@bot.command()
async def echo(ctx, *args):
    """Echoes back whatever you send it."""

    await ctx.send(' '.join(args))

# add all the cogs we have
# bot.add_cog(Voice(bot))
# bot.add_cog(Admin(bot))
# bot.add_cog(Text(bot))
bot.load_extension('cogs.voice')
bot.load_extension('cogs.admin')
bot.load_extension('cogs.text')

token = ''

try:
    token = import_module('secrets').discord_key
except NameError:
    token = environ['WHEATLEY_TOKEN']


bot.run(token)
