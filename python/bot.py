#! /usr/bin/python3

from importlib import import_module
from os import environ
from discord import AllowedMentions
from discord.ext import commands
# from cogs.admin import Admin
# from cogs.archive import Archive
# from cogs.voice import Voice
# from cogs.text import Text
# from cogs.poll import Poll
# from cogs.silly import Silly


bot = commands.Bot(
    command_prefix=commands.when_mentioned_or('!', '$'),
    allowed_mentions=AllowedMentions()
)


@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')


# add all the cogs we have
# bot.add_cog(Voice(bot))
# bot.add_cog(Admin(bot))
# bot.add_cog(Archive(bot))
# bot.add_cog(Text(bot))
# bot.add_cog(Poll(bot))
# bot.add_cog(Silly(bot))
bot.load_extension('cogs.voice')
bot.load_extension('cogs.admin')
bot.load_extension('cogs.archive')
bot.load_extension('cogs.text')
bot.load_extension('cogs.poll')
bot.load_extension('cogs.silly')

token = ''

try:
    token = import_module('secrets').discord_key
except NameError:
    token = environ['WHEATLEY_TOKEN']


bot.run(token)
