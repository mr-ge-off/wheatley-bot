async def _help(message, tokens):
    await message.channel.send('I\'m still learning. Gimme a break!')
    # TODO: implement this!

help_doc = (
    'help', {
        'desc': ' Displays help for a given topic',
        'callback': _help,
    }
)
