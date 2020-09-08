from importlib import import_module
from os import environ
import discord
from commands.list import all_commands
from commands.util import debug_print, tokenize

client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):

    # don't parse messages the bot itself sends
    if message.author == client.user:
        return

    command, tokens = await tokenize(message.content)

    if command:
        if command in all_commands.keys():
            await all_commands[command]['callback'](message, tokens)
        else:
            await message.channel.send(f'`{command}` is not a command!')

token = ''

try:
    token = import_module('secrets').discord_key
except NameError:
    token = environ['WHEATLEY_TOKEN']


client.run(token)