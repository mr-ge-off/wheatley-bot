from emoji import emojize
from util import tokenize, debug_print

async def parse_message(message):
    command, tokens = await tokenize(message.content)

    if command:
        if command in all_commands.keys():
            await all_commands[command]['callback'](message, tokens)
        else:
            await message.channel.send(f'`{command}` is not a command!')


async def list_commands(message, tokens):
    await message.channel.send(
        "Here's everything I know how to do:\n" +
        '\n'.join([f'!{item}: {value["desc"]}' for item, value in all_commands.items()])
    )

# TODO: add positional param for message to react to?
async def react(message, tokens):
    messages = await message.channel.history(limit=2).flatten()
    past_message = messages[1]
    if len(tokens) == 1:
        chars = list(dict.fromkeys(tokens[0].lower()))
        for char in chars:
            emoj = emojize(f':regional_indicator_{char}:', use_aliases=True)
            await past_message.add_reaction(emoj)
    else:
        for token in tokens:
            emoj = emojize(f':{token.lower()}:', use_aliases=True)
            if emoj.startswith(':'): continue
            await past_message.add_reaction(emoj)

async def hello(message, tokens):
    await message.channel.send('HI! I\'m Wheatley!')


all_commands = {
    'list': {
        'desc': 'Lists all commands',
        'callback': list_commands,
    },
    'hello': {
        'desc': 'Give a friendly greeting',
        'callback': hello,
    },
    'react': {
        'desc': 'Add text or emoji as reactions',
        'callback': react,
    }
}
