import discord
from commands import parse_message
from util import debug_print
from secrets import token

client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):

    # don't parse messages the bot itself sends
    if message.author == client.user:
        return

    await parse_message(message)

client.run(token)